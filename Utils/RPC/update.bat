title=update
rem update&&restart
taskkill /F /FI "WINDOWTITLE eq Node Server..." /FI "WINDOWTITLE ne update"
rem timeout /T 10 /NOBREAK
echo =====%date% %time%===== >> update_log.txt
git pull origin master >>update_log.txt 2>&1
timeout /T 10 /NOBREAK
start "" cmd  /k call startServer.bat
exit