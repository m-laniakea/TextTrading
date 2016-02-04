#!/bin/bash

echo Starting TextX Application in Python virtual environment 2.7...

sudo pip install virtualenv
virtualenv-2.7 nv
source nv/bin/activate
sudo pip install -r reqs.txt
python cmd.py runserver
