@echo off
setlocal

::set env paths for local
SET PYTHONPATH=%PYTHONPATH%;C:\Program Files\Side Effects Software\Houdini 19.5.368\houdini\python3.9libs;P:\pipeline\standalone_dev\libs;P:\pipeline\standalone_dev\libs\site-packages
SET PATH=%PATH%;C:\Program Files\Side Effects Software\Houdini 19.5.368\bin

::TASKKILL /F /IM "capoom.exe"
python runhda_dev.py
pause
endlocal