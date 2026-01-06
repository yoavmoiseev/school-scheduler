@echo off
echo Starting School Scheduler Web Application...
echo.

REM Change to script directory (where this BAT is)
cd /d "%~dp0"

REM Try to use venv python if exists, else fallback to system python
set "VENV_PY=.venv\Scripts\python.exe"
if exist "%VENV_PY%" (
	"%VENV_PY%" app.py
	if %ERRORLEVEL% neq 0 goto :error
	goto :end
)

REM Try to use 'python' from PATH
where python >nul 2>nul
if %ERRORLEVEL%==0 (
	python app.py
	if %ERRORLEVEL% neq 0 goto :error
	goto :end
)

REM Try to use 'py' launcher
where py >nul 2>nul
if %ERRORLEVEL%==0 (
	py app.py
	if %ERRORLEVEL% neq 0 goto :error
	goto :end
)

echo ERROR: Python not found. Please install Python 3.7+ and ensure it is in your PATH.
goto :pause

:error
echo.
echo ERROR: Failed to start app.py. Check your Python installation and dependencies.
goto :pause

:end
echo.
echo Application exited.
goto :pause

:pause
pause
