====================================================
@echo off
chcp 65001
rem 当前bat的作用

echo ==================begin========================

cls 
TITLE Node Server Manager...
cd %~dp0
cd ..
set BASE=%cd%

CLS 

ECHO. 
ECHO. * Node Server管理程序 * 
ECHO. * 			* 
ECHO. 

:MENU 

ECHO. * Node Server 进程list * 
tasklist /FI "WINDOWTITLE EQ Node Server..."

ECHO. 
ECHO. [1] 启动Node Server 
ECHO. [2] 关闭Node Server 
ECHO. [3] 更新Node Server 
ECHO. [4] 退 出 
ECHO. 

ECHO.请输入选择项目的序号:
set /p ID=
IF "%id%"=="1" GOTO start 
IF "%id%"=="2" GOTO stop 
IF "%id%"=="3" GOTO update 
IF "%id%"=="4" EXIT
PAUSE 

:start 
call :startNodeServer
GOTO MENU

:stop 
call :shutdownNodeServer
GOTO MENU

:update 
call :updateNodeServer
GOTO MENU

:shutdownNodeServer
ECHO. 
ECHO.关闭NodeServer...... 
cd %BASE%
python ./Utils/RPC/StopRPCServer.py
timeout /T 3 /NOBREAK
taskkill /F /FI "WINDOWTITLE EQ Node Server..."
taskkill /F /FI "WINDOWTITLE EQ Node Server..."
ECHO. OK.关闭NodeServer 进程
goto :eof

:startNodeServer
ECHO.
ECHO.启动NodeServer......
cd %BASE%
cd ./Utils/RPC/
start "Node Server..." cmd  /k call startServer.bat
GOTO MENU

:updateNodeServer
cd %BASE%
cd ./Utils/RPC/
start "update" cmd  /k call update.bat
GOTO MENU