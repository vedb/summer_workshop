import file_io
from collections import OrderedDict
import datetime
import warnings
import textwrap
import numpy as np
import os

class Session(object):
	def __init__(self, 
			scene=None, 
			folder=None, 
			lighting=None, 
			data_available=None,
			recording_duration=None, 
			start_time=None):
		"""Class for a data collection session for vedb project
		start_time : float
			Start time is the common start time for all clocks. Necessary for syncronization of disparate 
			frame rates and start lags

		"""


		inpt = locals()
		self.type = 'Session'
		for k, v in inpt.items():
			if not k in ['self', 'start_time', 'recording_duration']:
				setattr(self, k, v)
		BASE_PATH, folder = os.path.split(folder)
		self.folder = folder
		self._base_path = BASE_PATH
		self._paths = None
		self._start_time = start_time
		self._recording_duration = recording_duration
	
	def load(self, data_type, time_idx=None, frame_idx=None, **kwargs):
		"""
		Parameters
		----------
		data_type : string
			one of: 'world_camera', 'tracking_camera', 'eye_camera', 
			some data types have multiple sub-components; these can be accessed
			with colon syntax, e.g. data_type='odometry:location'
		time_idx : tuple
			(start time, end time) in seconds since the start of the session.
			Note that some streams (e.g. world_camera) may not start right at
			0 seconds, because they take some time to get started
		frame_idx : tuple
			(start_frame, end_frame)
		kwargs : dict
			passed to relevant loading function. 
			Note that for movie data, you can reshape and change the color format
			by using e.g. `size=(90, 120)` or `color='gray'` (see file_io.load_mp4)
		"""
		# Input check
		if (time_idx is None) and (frame_idx is None):
			raise ValueError("Please specify EITHER time_idx OR frame_idx, but not neither!")
		if (time_idx is not None) and (frame_idx is not None):
			raise ValueError("Please specify EITHER time_idx OR frame_idx, but not both!")
		if ':' in data_type:
			data_type, sub_type = data_type.split(':')
		else:
			sub_type = None
		tf, df = self.paths[data_type]
		tt = np.load(tf) - self.start_time
		if time_idx is not None:
			st, fin = time_idx
			ti = (tt > st) & (tt < fin)
			tt_clip = tt[ti]
			indices, = np.nonzero(ti)
			st_i, fin_i = indices[0], indices[-1]+1
		elif frame_idx is not None:
			st_i, fin_i = frame_idx
			tt_clip = tt[st_i:fin_i]
		if np.in1d(data_type, ['odometry', 'accel','gyro']):
			# Consider handling indices in load_msgpack; currently
			# an arg for idx is there, but not functional.
			dd = file_io.load_msgpack(df, idx=(st_i, fin_i))
			if sub_type is not None:
				dd = np.array([x[sub_type] for x in dd])
		else:
			dd = file_io.load_array(df, idx=(st_i, fin_i), **kwargs)
		return tt_clip, dd

	@property
	def start_time(self):
		if self._start_time is None:
			starts = []
			for k, v in self.paths.items():
				tfile, _ = v
				# look into memory mapping (e.g. kwarg `mmap_mode='r'`)
				# if this next line goes too slow
				try:
					# Kludge because first element of many timestamp 
					# arrays appears to be (spuriously) zero
					wait_frames = 1000
					tt = np.load(tfile)[:wait_frames]
					starts.append(np.min(tt[tt>0])) 
				except:
					print(f'Missing timestamps for {k}')
			self._start_time = np.min(starts)
		return self._start_time

	@property
	def recording_duration(self):
		"""Duration of recording in seconds"""
		if self._recording_duration is None:
			durations = []
			for k, v in self.paths.items():
				time_path, data_path = v
				if not os.path.exists(time_path):
					continue
				tt = np.load(time_path)
				stream_time = tt[-1] - self.start_time
				durations.append(stream_time)
			self._recording_duration = np.min(durations)
		return self._recording_duration
		
	@property
	def paths(self):
		if self._paths is None:
			to_find = ['world.mp4', 'eye0.mp4', 'eye1.mp4', 't265.mp4', 'odometry.pldata', 'gps.csv', 'gyro.pldata','accel.pldata'] # more?
			names = ['world_camera', 'eye_left', 'eye_right', 'tracking_camera', 'odometry', 'gps', 'gyro', 'accel']
			_paths = {}
			for fnm, nm in zip(to_find, names):
				tt, ee = os.path.splitext(fnm)
				data_path = os.path.join(self._base_path, self.folder, fnm)
				timestamp_path = os.path.join(self._base_path, self.folder, tt + '_timestamps.npy')
				if os.path.exists(data_path):
					_paths[nm] = (timestamp_path, data_path)
			self._paths = _paths
		return self._paths

	@classmethod
	def from_folder(cls, folder):
		"""Creates a new instance of this class from the given `docdict`.
		
		Parameters
		----------
		folder : string
			full path to folder name

		"""
		ob = cls.__new__(cls)
		print('\n>>> Importing folder %s'%folder)
		# Crop '/' from end of folder if exists
		if folder[-1] == os.path.sep:
			folder = folder[:-1]
		base_dir, folder_toplevel = os.path.split(folder)
		# Catch relative path, make into absolute path
		if folder_toplevel == '':
			folder_toplevel = base_dir
			base_dir = ''
		if (len(base_dir) == 0) or (base_dir[0] != '/'):
			base_dir = os.path.abspath(os.path.join(os.path.curdir, base_dir))

		def parse_resolution(res_string):
			out = res_string.strip('()').split(',')
			out = [int(x) for x in out]
			return out

		# Define recording device, w/ tag
		params = {}
		params['folder'] = folder_toplevel
		ob.__init__(*params)
		# set base directory to local base directory
		ob._base_path = base_dir
		return ob

	def __repr__(self):
		rstr = textwrap.dedent("""
			vedb_store.Session
			{d:>12s}: {date}
			""")
		return rstr.format(
			d='date', 
			date=self.folder,
			)


def get_image_region(image, center, size=(100,100), empty_value=np.nan):
    """Extract a rectangular region of an image
    
    Parameters
    ----------
    image : array
        image as a numpy array, should be (vdim, hdim) or (vdim, hdim, color)
    center : tuple
        (x,y) center, in absolute pixels or normalized (0-1) coordinates
    size : tuple, optional
        size of region to extract, (width, height)
    empty_value : scalar, optional
        value to use to pad the output if it goes off the edge of the image
    
    Returns
    -------
    cropped_image : array
    	cropped image of size `size`
    """
    vdim, hdim = image.shape[:2]
    x, y = center 
    if x <= 1:
        x = hdim * x
    if y <= 1: 
        y = vdim * y
    width, height = size
    left = int(x - width/2)
    right = left + width
    top = int(y - height/2)
    bottom = top + height
    
    left_pad = np.maximum(-left, 0)
    right_pad = np.maximum(right - hdim, 0)
    top_pad = np.maximum(-top, 0)
    bottom_pad = np.maximum(bottom - vdim, 0)
    
    left = np.maximum(0, left)
    right = np.minimum(hdim, right)
    top = np.maximum(0, top)
    bottom = np.minimum(vdim, bottom)
    
    box = image[top:bottom, left:right]
    if np.ndim(image) == 2:
        pad_dims = ((top_pad, bottom_pad), (left_pad, right_pad))
    elif np.ndim(image) == 3:
        pad_dims = ((top_pad, bottom_pad), (left_pad, right_pad), (0, 0))
    box = np.pad(box, pad_dims, mode='constant', constant_values=empty_value)
    return box