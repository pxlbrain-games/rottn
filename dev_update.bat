@ECHO off
ECHO ##################################
ECHO Updating Dependencies ...
ECHO ##################################
%~dp0venv\Scripts\python.exe -m pip install --upgrade pip
%~dp0venv\Scripts\python.exe -m pip install -r %~dp0requirements.txt
ECHO ##################################
ECHO Dev Update completed.
ECHO ##################################
PAUSE