rem update&&restart
timeout /T 10 /NOBREAK
git pull origin master
timeout /T 10 /NOBREAK
start "" cmd  /k call startServer.bat
