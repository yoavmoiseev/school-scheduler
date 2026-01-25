"""
Build script for creating standalone offline version of School Scheduler
Compatible with Windows 7, 8, 10, 11

This script uses PyInstaller to create a self-contained executable that:
- Includes Python runtime
- Includes all dependencies
- Bundles templates, static files, and data folders
- Requires no installation
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print("✓ PyInstaller found")
        return True
    except ImportError:
        print("✗ PyInstaller not found")
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
        print("✓ PyInstaller installed")
        return True

def create_spec_file():
    """Create PyInstaller spec file for the application"""
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('static', 'static'),
        ('data', 'data'),
        ('ExcelExamples', 'ExcelExamples'),
        ('models', 'models'),
        ('routes', 'routes'),
        ('services', 'services'),
        ('config.py', '.'),
        ('source_consts.py', '.'),
    ],
    hiddenimports=[
        'flask',
        'flask_cors',
        'openpyxl',
        'openpyxl.cell._writer',
        'openpyxl.styles',
        'openpyxl.workbook',
        'openpyxl.worksheet',
        'jinja2',
        'werkzeug',
        'click',
        'itsdangerous',
        'markupsafe',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SchoolScheduler',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    coerce_macros=True,
    entitlements_file=None,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SchoolScheduler',
)
"""
    
    with open('school_scheduler.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✓ Created PyInstaller spec file")

def build_executable():
    """Build the executable using PyInstaller"""
    print("\nBuilding executable with PyInstaller...")
    print("This may take several minutes...\n")
    
    try:
        subprocess.check_call([
            sys.executable, '-m', 'PyInstaller',
            '--clean',
            'school_scheduler.spec'
        ])
        print("\n✓ Build completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed: {e}")
        return False

def create_launcher():
    """Create a simple launcher batch file"""
    launcher_content = """@echo off
title School Scheduler - Offline Version
cls
echo ================================================================
echo                    SCHOOL SCHEDULER
echo                     Offline Version
echo ================================================================
echo.
echo Starting server...
echo.
echo The application will open in your browser automatically.
echo.
echo TO STOP THE SERVER: Close this window or press Ctrl+C
echo ================================================================
echo.

REM Start the application and open browser
start "" "SchoolScheduler.exe"

REM Wait a moment for server to start
timeout /t 2 /nobreak >nul

REM Open browser
start http://127.0.0.1:5000

echo.
echo Server is running!
echo Access the application at: http://127.0.0.1:5000
echo.
echo Press any key to stop the server...
pause >nul
"""
    
    dist_path = Path('dist/SchoolScheduler')
    if dist_path.exists():
        launcher_path = dist_path / 'START_HERE.bat'
        with open(launcher_path, 'w', encoding='utf-8') as f:
            f.write(launcher_content)
        print(f"✓ Created launcher: {launcher_path}")
        return True
    else:
        print(f"✗ Distribution folder not found: {dist_path}")
        return False

def create_readme():
    """Create README for offline version"""
    readme_content = """# School Scheduler - Offline Version

## How to Use

1. **Start the Application**
   - Double-click on `START_HERE.bat`
   - The server will start and your browser will open automatically

2. **Access the Application**
   - The application will open at: http://127.0.0.1:5000
   - If the browser doesn't open automatically, open it manually and go to the above address

3. **Stop the Application**
   - Close the command window
   - OR press Ctrl+C in the command window

## System Requirements

- Windows 7 / 8 / 10 / 11
- No internet connection required
- No Python installation required
- All dependencies included

## Features

- Complete offline operation
- All data stored locally in Excel files
- Multi-language support (English, Hebrew, Russian)
- Automatic schedule generation
- PDF export capability

## Troubleshooting

**Problem:** Application doesn't start
- Make sure no other program is using port 5000
- Try running as Administrator

**Problem:** Browser doesn't open
- Manually open your browser and go to: http://127.0.0.1:5000

**Problem:** "Port already in use" error
- Close any other instance of the application
- Check if another program is using port 5000

## Data Location

All your data is stored in the `data` folder:
- `data/users/[username]/schedule_data.xlsx` - Your schedule data

To backup your data, simply copy the entire folder to another location.

## Support

For issues or questions, visit:
https://github.com/yoavmoiseev/school-scheduler

---
Built with PyInstaller for offline use
Compatible with Windows 7/8/10/11
"""
    
    dist_path = Path('dist/SchoolScheduler')
    if dist_path.exists():
        readme_path = dist_path / 'README.txt'
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"✓ Created README: {readme_path}")
        return True
    else:
        print(f"✗ Distribution folder not found: {dist_path}")
        return False

def copy_data_folders():
    """Copy data and example folders to distribution"""
    dist_path = Path('dist/SchoolScheduler')
    
    if not dist_path.exists():
        print(f"✗ Distribution folder not found: {dist_path}")
        return False
    
    folders_to_copy = ['data', 'ExcelExamples']
    
    for folder in folders_to_copy:
        src = Path(folder)
        dst = dist_path / folder
        
        if src.exists():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"✓ Copied {folder} to distribution")
        else:
            # Create empty folder if it doesn't exist
            dst.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created empty {folder} folder")
    
    return True

def main():
    """Main build process"""
    print("=" * 60)
    print("Building School Scheduler - Offline Version")
    print("Target: Windows 7/8/10/11")
    print("=" * 60)
    print()
    
    # Step 1: Check PyInstaller
    if not check_pyinstaller():
        print("Failed to install PyInstaller")
        return 1
    
    print()
    
    # Step 2: Create spec file
    create_spec_file()
    print()
    
    # Step 3: Build executable
    if not build_executable():
        print("\nBuild failed!")
        return 1
    
    print()
    
    # Step 4: Copy data folders
    copy_data_folders()
    print()
    
    # Step 5: Create launcher
    create_launcher()
    print()
    
    # Step 6: Create README
    create_readme()
    print()
    
    print("=" * 60)
    print("✓ BUILD COMPLETE!")
    print("=" * 60)
    print()
    print("The offline version is ready in: dist\\SchoolScheduler")
    print()
    print("To distribute:")
    print("1. Zip the 'dist\\SchoolScheduler' folder")
    print("2. Users extract the zip")
    print("3. Users double-click 'START_HERE.bat'")
    print()
    print("No installation required!")
    print("=" * 60)
    
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nBuild cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
