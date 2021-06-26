# Environment setup

export name=summer_workshop

# Create initial environment
mamba env create -f environment.yml

# Activate it
conda activate $name

# Make source code directory for git libraries
if [ -d ~/Code ]
	then
		:
	else
	mkdir ~/Code
fi
cd ~/Code/

# Retrieve and install libraries from git...
# ... for loading files:
if [ -d file_io ]
then
	:
else
	git clone git@github.com:vedb/file_io.git
fi
cd file_io
python setup.py install
cd ..
# ... for plotting:
if [ -d plot_utils ]
then
	:
else
	git clone git@github.com:piecesofmindlab/plot_utils.git
fi
cd plot_utils
python setup.py install
cd ..
cd ..

ipython kernel install --user --name $name
