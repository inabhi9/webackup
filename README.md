#Webackup

An open source online backup tool to transfer your data to various cloud storage provider like Dropbox.com, Box.com, FTP and etc...

## Technology stack
---
* Python
* SQLite3
* APScheduler
* Flask
* Twitter Bootstrap
* Peewee

##Dependancies
---
* Python 2.6+
* Python setuptools
* mongodump
* mysqldump

##Installation
---
sudo apt-get install python-dev
git clone git@bitbucket.org:inabhi9/webackup.git
cd webackup/
pip install -r requirements.txt
chmod +x run.py

#Usage
---
./run.py
This will start server listening on 127.0.0.1:2587. If you want to make it global edit run.py and change 127.0.0.1 to 0.0.0.0

##Contribution
---
Webackup will always remain free and open source. Feel free to fork and merge Webackup to make it more powerful and robust backup tool.



##Changelog
---

#### version 0.1
* Destination: FTP
* Sources: MySQL, MongoDB, Local file system
* Supports archiving before transfer
* Interval based scheduling.
* Basic report
* Basic profile management
* Email notification