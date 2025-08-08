#!/bin/bash

apt-get update && apt-get install -y python3-sphinx
pip3 install virtualenv sphinx_rtd_theme
VENV=$HOME/.venv
rm -rf $VENV > /dev/null
virtualenv -p python3 --always-copy $VENV
source $VENV/bin/activate

cd ../docs
make clean
make html