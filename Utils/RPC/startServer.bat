timeout /T 10 /NOBREAK
cd %~dp0
cd ../..
title=Node Server...
python ./Utils/RPC/RPCServer.py

pause