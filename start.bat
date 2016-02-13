@ECHO OFF
PUSHD %~dp0

ECHO Starting TextX Application in Python virtual environment 2.7...

SET PATH=C:\Python27;C:\Python27\Lib;C:\Python27\DLLs;C:\Python27\Scripts
SET PYTHONPATH=C:\Python27;C:\Python27\Lib;C:\Python27\DLLs;C:\Python27\Scripts
SET PYTHONHOME=C:\Python27
pip install virtualenv
virtualenv-2.7 nv
nv\Scripts\activate.bat
pip install -r reqs.txt
python cmd.py runserver

POPD