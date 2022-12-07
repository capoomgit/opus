@echo off
setlocal
SET PYTHONPATH=%PYTHONPATH%;C:\Users\capoom\AppData\Local\ov\pkg\isaac_sim-2022.1.1\site


:: The executable path will be where python is located. So we set Cabonite app path through env var:
set CARB_APP_PATH=C:\Users\capoom\AppData\Local\ov\pkg\isaac_sim-2022.1.1\kit
set ISAAC_PATH=C:\Users\capoom\AppData\Local\ov\pkg\isaac_sim-2022.1.1\
set EXP_PATH=C:\Users\capoom\AppData\Local\ov\pkg\isaac_sim-2022.1.1\apps

:: By default use our python, but allow overriding it by checking if PYTHONEXE env var is defined:
IF "%PYTHONEXE%"=="" (
    set PYTHONEXE="C:\Users\capoom\AppData\Local\ov\pkg\isaac_sim-2022.1.1\kit\python\pythonw.exe"
)

call %PYTHONEXE% %*

if errorlevel 1 ( goto ErrorRunningPython )

:Success
endlocal
exit /B 0

:ErrorRunningPython
echo There was an error running python.
endlocal
exit /B 1
