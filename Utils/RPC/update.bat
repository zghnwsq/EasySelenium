title=update
rem update&&restart
taskkill /F /FI "WINDOWTITLE eq Node Server..." /FI "WINDOWTITLE ne update"
git pull origin master >>update_log.txt
rem timeout /T 10 /NOBREAK
start "" cmd  /k call startServer.bat
exit