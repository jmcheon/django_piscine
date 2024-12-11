#!/bin/bash

# setup venv
python3 -m venv django_venv/
source ./django_venv/bin/activate

# pip install
pip install -r requirements.txt