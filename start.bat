@ECHO OFF
PUSHD %~dp0

ECHO Starting TextX Application in Python virtual environment 2.7...

SET PYTHONPATH=C:\Python27;C:\Python27\Lib;C:\Python27\DLLs
SET PYTHONHOME=C:\Python27
pip install virtualenv
virtualenv-2.7 nv
source nv/bin/activate
pip install -r reqs.txt
python cmd.py runserver

POPD