@echo off



IF exist %LOCALAPPDATA%\Capoom_Python39 (echo python already exist) ELSE (mkdir %LOCALAPPDATA%\Capoom_Python39 && xcopy /S P:\pipeline\standalone\Capoom_Python39 %LOCALAPPDATA%\Capoom_Python39)

SET /P ISCLIENT=Is this client (Y/N)?

IF /I "%ISCLIENT%" EQU "Y" GOTO CLIENT
IF /I "%ISCLIENT%" EQU "N" GOTO END

:CLIENT
copy "P:\pipeline\standalone\client\capoomClient.bat"  "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\capoomClient.bat"

timeout /t 1 /nobreak
start cmd.exe /c "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\capoomClient.bat"

GOTO END




:END
echo Installed
pause


