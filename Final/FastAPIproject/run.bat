@echo off
cd /d "%~dp0"
echo Starting FastAPI Server...
echo The server will use http://127.0.0.1:5000/ or the next free port if 5000 is busy.

set "PYTHON_CMD="

if exist ".venv311\Scripts\python.exe" (
    ".venv311\Scripts\python.exe" --version >nul 2>&1 && set "PYTHON_CMD=.venv311\Scripts\python.exe"
)

if not defined PYTHON_CMD if defined VIRTUAL_ENV if exist "%VIRTUAL_ENV%\Scripts\python.exe" (
    "%VIRTUAL_ENV%\Scripts\python.exe" --version >nul 2>&1 && set "PYTHON_CMD=%VIRTUAL_ENV%\Scripts\python.exe"
)

if not defined PYTHON_CMD if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" --version >nul 2>&1 && set "PYTHON_CMD=.venv\Scripts\python.exe"
)

if not defined PYTHON_CMD (
    python --version >nul 2>&1 && set "PYTHON_CMD=python"
)

if not defined PYTHON_CMD (
    echo Could not find a working Python installation.
    echo Install Python from https://www.python.org/downloads/ and check "Add python.exe to PATH".
    pause
    exit /b 1
)

"%PYTHON_CMD%" run_fastapi.py
pause
