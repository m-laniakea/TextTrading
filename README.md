# TextX

Getting started on Unix:

    Install:
      Python 2.7 (package)

    Run: (or run start.sh elevated)
      # virtualenv-2.7 nv
      # source nv/bin/activate
      # sudo pip install -r reqs.txt
      # ./cmd.py runserver

Getting started on Windows:

    Install:
      Download Python 2.7.*, link: https://www.python.org/downloads/
      - Install in the default "C:\Python27" or suffer custom startup commands
      - Be sure to enable "Add python.exe to Path" so CMD can find it
      - Reboot after installation
    
    Run: (or run start.bat as Administrator)
      # SET PATH=C:\Python27;C:\Python27\Lib;C:\Python27\DLLs;C:\Python27\Scripts
      # SET PYTHONPATH=C:\Python27;C:\Python27\Lib;C:\Python27\DLLs
      # SET PYTHONHOME=C:\Python27
      # pip install virtualenv
      # virtualenv-2.7 nv
      # vn\Scripts\activate.bat
      # pip install -r reqs.txt
      # python cmd.py runserver

Getting started on Mac OS:

    Install Python 2.7 with Easy Install
    - Open Terminal
    - sudo easy_install pip
    
    Run: (use Unix run instructions)
      
Preparing the new database:

    Population on Unix: (in virtual env)
      # ./cmd.py shell
      # User.populate()
      Ctrl + D
      # ./cmd.py runserver

    Population on Windows: (in virtual env)
      # python .\cmd.py shell
      # User.populate()
      Ctrl + C
      # python .\cmd.py runserver
    
    Access:
      Since the GitHub server is public, we will not use real emails.  Spam bots will have lots of fun hitting these fake addresses. 
      
      Use Discord username + "@uw.edu", e.g. Ruby@uw.edu, password is "ftt"
      If you used your NetID as your discord name, it will be your first name. 
      For example: Erick is just erick@uw.edu

Viewing the site:

    Open "http://localhost:5000" in your web browser

Initializing the database with filler content (model definitions):

    On Unix: (in virtual env)
      # ./cmd.py shell
      # db.create_all()
      Ctrl + D
    
    On Windows: (in virtual env)
      # python .\cmd.py shell
      # db.create_all()
      Ctrl + C
