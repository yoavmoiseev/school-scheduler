@echo off
REM Quick test to verify offline resources are working
title Testing Offline Resources...
cls

echo ================================================================
echo   TESTING OFFLINE RESOURCES
echo ================================================================
echo.

cd /d "%~dp0"

echo Checking offline dependencies...
echo.

echo [1/5] Checking Bootstrap CSS...
if exist "static\vendor\bootstrap\bootstrap.min.css" (
    echo    ✓ Bootstrap CSS found
) else (
    echo    ✗ Bootstrap CSS MISSING!
    set ERROR=1
)

echo [2/5] Checking Bootstrap JS...
if exist "static\vendor\bootstrap\bootstrap.bundle.min.js" (
    echo    ✓ Bootstrap JS found
) else (
    echo    ✗ Bootstrap JS MISSING!
    set ERROR=1
)

echo [3/5] Checking jQuery...
if exist "static\vendor\jquery\jquery-3.6.0.min.js" (
    echo    ✓ jQuery found
) else (
    echo    ✗ jQuery MISSING!
    set ERROR=1
)

echo [4/5] Checking templates...
if exist "templates\base.html" (
    findstr /C:"vendor/bootstrap" "templates\base.html" >nul
    if !ERRORLEVEL!==0 (
        echo    ✓ Templates updated for offline
    ) else (
        echo    ✗ Templates still use CDN!
        set ERROR=1
    )
) else (
    echo    ✗ Templates MISSING!
    set ERROR=1
)

echo [5/5] Checking build scripts...
if exist "BUILD_OFFLINE.bat" (
    echo    ✓ Build script found
) else (
    echo    ✗ Build script MISSING!
    set ERROR=1
)

echo.
echo ================================================================

if defined ERROR (
    echo   ✗ SOME CHECKS FAILED!
    echo.
    echo   Run: download_offline_deps.py
    echo   to download missing dependencies
) else (
    echo   ✓ ALL CHECKS PASSED!
    echo.
    echo   Your application is ready for offline use.
    echo   Run BUILD_OFFLINE.bat to create distributable version.
)

echo ================================================================
echo.
pause
