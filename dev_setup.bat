@ECHO off
ECHO Only run this once!
ECHO Create venv, add project path to it and install all dependencies?
SET /p continue=[y/n] 
IF %continue%==n EXIT
ECHO Input path to Python 3.6+ Installation
SET /p path=(Path to executable): 
ECHO ##################################
ECHO Creating Virtual Environment ...
ECHO ##################################
MKDIR %~dp0venv
%path% -m venv %~dp0venv
ECHO Appending Development Directory to PYTHONPATH ...
> %~dp0venv\Lib\site-packages\bossfight.pth ECHO %~dp0bossfight.client\
>> %~dp0venv\Lib\site-packages\bossfight.pth ECHO %~dp0bossfight.core\
>> %~dp0venv\Lib\site-packages\bossfight.pth ECHO %~dp0bossfight.server\
ECHO ##################################
ECHO Installing Dependencies ...
ECHO ##################################
%~dp0venv\Scripts\python.exe -m pip install --upgrade pip
%~dp0venv\Scripts\python.exe -m pip install --upgrade setuptools
%~dp0venv\Scripts\python.exe -m pip install -r %~dp0requirements.txt
%~dp0venv\Scripts\pypy3.exe -m pip install --upgrade pip
%~dp0venv\Scripts\pypy3.exe -m pip install --upgrade setuptools
%~dp0venv\Scripts\pypy3.exe -m pip install -r %~dp0requirements.txt
ECHO ##################################
ECHO Dev Setup completed.
ECHO Use .\venv environment for testing
ECHO and development.
ECHO ##################################
PAUSE