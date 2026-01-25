@echo off
REM =============================================================
REM   BUILD OFFLINE VERSION OF SCHOOL SCHEDULER
REM   Compatible with Windows 7, 8, 10, 11
REM =============================================================

title Building Offline Version...
cls

echo ================================================================
echo           SCHOOL SCHEDULER - BUILD OFFLINE VERSION
echo ================================================================
echo.
echo This script will create a standalone offline version that:
echo   - Works without internet connection
echo   - Requires no Python installation
echo   - Can be distributed as a simple ZIP file
echo.
echo Compatible with: Windows 7, 8, 10, 11
echo.
echo ================================================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check if Python is available
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python 3.7 or higher and add it to PATH
    echo.
    pause
    exit /b 1
)

echo [1/3] Installing dependencies...
echo.
python -m pip install --upgrade pip
python -m pip install pyinstaller flask flask-cors openpyxl python-dotenv
echo.

echo [2/3] Downloading offline resources (Bootstrap, jQuery)...
echo.
python download_offline_deps.py
if %ERRORLEVEL% neq 0 (
    echo.
    echo ERROR: Failed to download offline dependencies
    echo.
    pause
    exit /b 1
)
echo.

echo [3/3] Building standalone executable...
echo This may take several minutes, please wait...
echo.
python build_offline_version.py
if %ERRORLEVEL% neq 0 (
    echo.
    echo ERROR: Build failed
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================================
echo                    BUILD SUCCESSFUL!
echo ================================================================
echo.
echo The offline version is ready in: dist\SchoolScheduler
echo.
echo To distribute:
echo   1. Zip the 'dist\SchoolScheduler' folder
echo   2. Send the ZIP file to users
echo   3. Users extract and double-click 'START_HERE.bat'
echo.
echo No installation required on user computers!
echo ================================================================
echo.
pause
