#!/bin/bash

python -m pip install flake8
#python -m pip install autopep8
#find . -name "*.py" -exec autopep8 --in-place --ignore=E501 --max-line-length=160 {} \;
python -m flake8 --ignore=E501 --max-line-length=160
