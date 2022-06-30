#!/bin/bash

#
# Install the python library requirements
#
sudo apt-get update
sudo apt-get install python3.9-venv python3-pip libpython3.9-dev libmysqlclient-dev
python3.9 -m venv venv
source venv/bin/activate
export PYTHONPATH=`pwd`
echo "PYTHONPATH=${PYTHONPATH}"
pip install --upgrade pip
pip install safety
pip install -r requirements.txt
