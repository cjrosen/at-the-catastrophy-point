#!/bin/bash

ENV_NAME="venv"

# Init the virtual env
python3 -m venv $ENV_NAME
source $ENV_NAME/bin/activate

# Install Python requirements
pip install -r requirements.txt

#pip install --editable .

# For Jupyter support
# Skip this step if you don't need Jupyter support
# https://anbasile.github.io/programming/2017/06/25/jupyter-venv/
pip install jupyterlab
pip install notebook