@ECHO off
ECHO Only run this once!
ECHO Create venv, add project path to it and install all dependencies?
SET /p continue=[y/n] 
IF %continue%==n EXIT
ECHO Input path to Python 3.6+ installation
SET /p path=(the directory that contains the python.exe, without a slash at the end): 
ECHO ##################################
ECHO Creating Virtual Environment ...
ECHO ##################################
MKDIR %~dp0venv
%path%\python.exe -m venv %~dp0venv
ECHO Appending Development Directory to PYTHONPATH ...
> %~dp0venv\Lib\site-packages\bossfight.pth ECHO %~dp0bossfight.client\
>> %~dp0venv\Lib\site-packages\bossfight.pth ECHO %~dp0bossfight.core\
>> %~dp0venv\Lib\site-packages\bossfight.pth ECHO %~dp0bossfight.server\
ECHO ##################################
ECHO Installing Dependencies ...
ECHO ##################################
%~dp0venv\Scripts\python.exe -m pip install --upgrade pip
%~dp0venv\Scripts\python.exe -m pip install -r %~dp0requirements.txt
ECHO ##################################
ECHO Dev Setup completed.
ECHO Use .\venv environment for testing
ECHO and development.
ECHO ##################################
PAUSE