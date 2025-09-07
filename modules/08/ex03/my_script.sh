#!/bin/bash

# setup venv
# python3 -m venv django_venv/
/opt/homebrew/bin/python3.11 -m venv django_venv/

source ./django_venv/bin/activate

# pip install
pip install --upgrade pip
pip install -r requirements.txt