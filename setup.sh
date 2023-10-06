#!/usr/bin/bash

apt update
apt upgrade
apt install python3-pip

apt install python3.10-venv
python3 -m venv env
source env/bin/activate

python3 -m pip install flask
pip3 -r requirements.txt

python3 main.py