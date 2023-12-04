#!/usr/bin/bash

apt update
apt upgrade
apt install python3-pip
pip3 install -r requirements.txt
python3 main.py 80