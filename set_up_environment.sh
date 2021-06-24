# Environment setup

export name=summer_workshop_test

# Create initial environment
mamba env create -f environment.yml

# Activate it
conda activate $name

# Retrieve and install libraries from git...
# ... for loading files:
git clone git@github.com:vedb/file_io.git
cd file_io
python setup.py install
cd ..
# ... for plotting:
git clone git@github.com:piecesofmindlab/plot_utils.git
cd plot_utils
python setup.py install
cd ..

ipython kernel install --user --name $name