#!/bin/bash

ENV_NAME="mohr"

# Init the virtual env
conda create --name $ENV_NAME python==3.8
conda activate $ENV_NAME


conda install poppler # for https://pypi.org/project/pdf2image/

pip install -r requirements.txt

#pip install --editable .

# For Jupyter support
# Skip this step if you don't need Jupyter support
# https://anbasile.github.io/programming/2017/06/25/jupyter-venv/
pip install jupyterlab notebook


# 'conda deactivate' to leave venv
# 'conda remove --name $ENV_NAME' to remove venv