@echo off
setlocal

::set env paths for local
SET PYTHONPATH=%PYTHONPATH%;P:\pipeline\standalone_dev\libs;P:\pipeline\standalone_dev\libs\site-packages
"%LOCALAPPDATA%\Capoom_Python39\python.exe" migrate_parms.py

endlocal
pause