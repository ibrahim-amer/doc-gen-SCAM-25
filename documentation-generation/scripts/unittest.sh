#!/bin/bash
set -e

pip install poetry
cd ..
poetry install
poetry run coverage run
poetry run coverage report