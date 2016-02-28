@ECHO OFF
PUSHD %~dp0

ECHO Starting TextX Application in Python virtual environment 2.7...

:: Show Windows and Python where to find our Python executables
SET PATH=C:\Python27;C:\Python27\Lib;C:\Python27\DLLs;C:\Python27\Scripts
SET PYTHONPATH=C:\Python27;C:\Python27\Lib;C:\Python27\DLLs;C:\Python27\Scripts
SET PYTHONHOME=C:\Python27

:: Installs Python virtual environment, creates and activates one for v2.7
pip install virtualenv
virtualenv-2.7 nv
call nv\Scripts\activate.bat

:: Install prerequisites (in the virtual environment) and run the server
pip install -r reqs.txt
python cmd.py runserver

POPD