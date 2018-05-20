@ECHO off
ECHO ##################################
ECHO Updating Dependencies ...
ECHO ##################################
%~dp0venv\Scripts\python.exe -m pip install --upgrade pip
%~dp0venv\Scripts\python.exe -m pip install --upgrade setuptools
%~dp0venv\Scripts\python.exe -m pip install --upgrade -r %~dp0requirements.txt
%~dp0venv\Scripts\pypy3.exe -m pip install --upgrade pip
%~dp0venv\Scripts\pypy3.exe -m pip install --upgrade setuptools
%~dp0venv\Scripts\pypy3.exe -m pip install --upgrade -r %~dp0requirements.txt
ECHO ##################################
ECHO Dev Update completed.
ECHO ##################################
PAUSE