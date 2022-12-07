@echo off



IF exist %LOCALAPPDATA%\CapoomClient ( echo CapoomClient exists && RMDIR %LOCALAPPDATA%\CapoomClient /S /Q ) ELSE ( echo CapoomClient does not exist )
mkdir %LOCALAPPDATA%\CapoomClient
echo CapoomClient created
xcopy /s P:\pipeline\standalone\client %LOCALAPPDATA%\CapoomClient
cd %LOCALAPPDATA%\CapoomClient

start cmd.exe /c "cd %LOCALAPPDATA%\CapoomClient & startClient.bat" -WindowStyle Hidden

