#!/bin/bash


echo 'in startup.sh, installing reqs'
pip install -r requirements.txt


python3 ./utils/coordinator.py