@ECHO off
ECHO ##################################
ECHO Updating Dependencies ...
ECHO ##################################
%~dp0venv\Scripts\python.exe -m pip install --upgrade pip
%~dp0venv\Scripts\python.exe -m pip install --upgrade setuptools
%~dp0venv\Scripts\python.exe -m pip install --upgrade -r %~dp0requirements.txt
%~dp0pypyvenv\Scripts\pypy3.exe -m pip install --upgrade pip
%~dp0pypyvenv\Scripts\pypy3.exe -m pip install --upgrade setuptools
%~dp0pypyvenv\Scripts\pypy3.exe -m pip install --upgrade -r %~dp0requirements_pypy.txt
ECHO ##################################
ECHO Dev Update completed.
ECHO ##################################
PAUSE