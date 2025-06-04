@echo off
REM Aktifkan virtual environment
call "%~dp0venv\Scripts\activate"

python "%~dp0gcommit.py" %*

REM Nonaktifkan virtual environment
call "%~dp0venv\Scripts\deactivate"

