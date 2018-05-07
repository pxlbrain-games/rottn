@ECHO off
ECHO Only run this once!
ECHO Create venv, add path to PYTHONPATH and install dependencies?
SET /p continue=[y/n] 
IF %continue%==n EXIT
SET /p path=Input path to Python Distribution (with backslashes): 
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
%~dp0venv\Scripts\python.exe -m pip install pytest
%~dp0venv\Scripts\python.exe -m pip install pyglet
%~dp0venv\Scripts\python.exe -m pip install cocos2d
%~dp0venv\Scripts\python.exe -m pip install u-msgpack-python
ECHO ##################################
ECHO Dev Setup completed.
ECHO Use .\venv environment for testing
ECHO ##################################
PAUSE