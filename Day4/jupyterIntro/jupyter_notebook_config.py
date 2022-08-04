# Configuration file for jupyter-notebook for BDSS summer 2022 specifically

## The full path to an SSL/TLS certificate file.
c.NotebookApp.certfile = '/home/bdss_student/.openssl/notebook_certification.pem'
c.NotebookApp.keyfile = '/home/bdss_student/.openssl/notebook_key.key'

## The IP address the notebook server will listen on.
c.NotebookApp.ip = '*'

## Whether to open in a browser after starting.
#  The specific browser used is platform- dependent and determined by the python standard library `webbrowser` module, unless it is overridden using the --browser (NotebookApp.browser) configuration option.
#  Default: True
c.NotebookApp.open_browser = False
