#!/bin/bash

# setup venv
python3 -m venv local_lib/
source local_lib/bin/activate

# pip version
python3 -m pip3 --version

# pip install
python3 -m pip3 install --log path_install.log --upgrade --force-reinstall  git+https://github.com/jaraco/path.py.git

python3 my_program.py
