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
	
	def load(self, data_type, time_idx=(0, 10), frame_idx=None, **kwargs):
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
		else:
			raise ValueError('Please specify either `time_idx` or `frame_idx`')
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
	def datetime(self):
		dt = datetime.datetime.strptime(self.date, '%Y_%m_%d_%H_%M_%S')
		return dt
	
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
		# Set date	(& be explicit about what constitutes date)	
		session_date = folder_toplevel
		try:
			# Assume year_month_day_hour_min_second for date specification in folder title
			dt = datetime.datetime.strptime(session_date, '%Y_%m_%d_%H_%M_%S')
		except:
			print('Date not parseable!')

		def parse_resolution(res_string):
			out = res_string.strip('()').split(',')
			out = [int(x) for x in out]
			return out

		# Define recording device, w/ tag
		params = {}
		params['folder'] = folder_toplevel
		params['date'] = session_date
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
			date=self.date,
			)
