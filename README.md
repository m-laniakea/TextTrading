# TextX

Getting started on Unix:

    Install:
      Python 2.7 (package)

    Run: (or run start.sh elevated)
      # virtualenv-2.7 nv
      # source nv/bin/activate
      # pip install -r reqs.txt
      # python cmd.py runserver
      
Using the database:

    Population:
      (In nv environment)
      # ./cmd shell
      # User.populate()
      Ctrl + D
      # ./cmd runserver
    
    Access:
      Use Discord username + "@uw.edu", e.g. Ruby@uw.edu, password is "flipthetable"
      Erick is just erick@uw.edu
	

Getting started on Windows:

    Install:
      Download Python 2.7.*, link: https://www.python.org/downloads/
      - Install in the default "C:\Python27" or suffer custom startup commands
      - Be sure to enable "Add python.exe to Path" so CMD can find it
      - Reboot after installation
    
    Run: (or run start.bat as Administrator)
      # SET PYTHONPATH=C:\Python27;C:\Python27\Lib;C:\Python27\DLLs
      # SET PYTHONHOME=C:\Python27
      # pip install virtualenv
      # virtualenv-2.7 nv
      # source nv/bin/activate
      # pip install -r reqs.txt
      # python cmd.py runserver

Viewing the site:

	Open "http://localhost:5000" in your web browser

Initializing a blank database from model definitions:

      # python cmd.py shell
      # db.create_all()
      Ctrl + D
