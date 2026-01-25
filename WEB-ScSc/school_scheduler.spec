# -*- mode: python ; coding: utf-8 -*-

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
