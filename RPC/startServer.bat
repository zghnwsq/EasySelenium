timeout /T 3 /NOBREAK
cd %~dp0
cd ..
title=Node Server...
python ./RPC/RPCServer.py

pause