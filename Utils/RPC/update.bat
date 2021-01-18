timeout /T 10 /NOBREAK
git pull -u origin master:master
timeout /T 60 /NOBREAK
start “” cmd  /k call startServer.bat
