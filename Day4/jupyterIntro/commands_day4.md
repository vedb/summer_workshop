# Commands for python & jupyter

Set up bash / git on your local machine: (from Anaconda powershell ON YOUR DESKTOP)
* `conda install git`

Log in to virtual machine and do some configuration of jupyter on your remote machines:
`bash run_jupyter_config.sh`

General way to create a new conda environment:
* `conda env create -n <environment name> python=3.8`

Create a new conda environment with a couple useful packages:
* `conda create -n plot_demo_env python=3.8 ipython matplotlib numpy ipython jupyter`

Activate the environment
* `conda activate plot_demo_env`

Start python:
* `python`

Start ipython:
* `ipython`

Start jupyter notebook
* `jupyter notebook`

(All same commands apply locally & remote, but the running jupyter notebook is a bit tricky to access remotely: you find it at `<node_name>.acs.unr.edu:8888`, ignore warnings, and enter password)

(Run demo in jupyter notebook)

Install a new library (aka module aka package) into this environment
* `conda install opencv`

Gaaa! that doesn't work! We need to specify a *channel* in anaconda's online store:
* `conda install -c conda-forge opencv`

# Reminders for hotkeys
* `ctrl-c` : stop code from running
* `ctrl-d` : disconnect from ssh or current terminal session

