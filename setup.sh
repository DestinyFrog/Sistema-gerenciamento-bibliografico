#!/usr/bin/bash

apt update
apt upgrade
apt install python3-pip

apt install python3.10-venv
python3 -m venv env
source env/bin/activate

python3 -m pip install flask
python3 -m pip install waitress

python3 serv/main.py