# Configure jupyter to serve over web!

# create certification files
mkdir $HOME/.openssl/
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout $HOME/.openssl/notebook_key.key -out $HOME/.openssl//notebook_certification.pem

conda install jupyter

# Set up configuration file for jupyter
jupyter notebook --generate-config

# Set password for notebook
jupyter notebook password

# Copy config file
cp jupyter_notebook_config.py ~/.jupyter/