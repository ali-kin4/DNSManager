# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for DNS Manager Pro
Build command: pyinstaller dns_manager.spec
"""

import sys
from pathlib import Path

block_cipher = None

# Get version
version_file = Path('version.py')
version_info = {}
exec(version_file.read_text(), version_info)
app_version = version_info['__version__']

a = Analysis(
    ['dns_manager.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('logo.svg', '.'),
        ('version.py', '.'),
        ('updater.py', '.'),
    ],
    hiddenimports=[
        'PIL._tkinter_finder',
        'darkdetect',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'pytest',
        'setuptools',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DNSManagerPro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI app, no console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='logo.ico',
    version_file=None,  # Can add version_info.txt later
    uac_admin=True,  # Request admin rights
    uac_uiaccess=False,
)

# Optional: Create version info file for Windows
version_info_content = f"""
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({','.join(app_version.split('.'))}),
    prodvers=({','.join(app_version.split('.'))}),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Ali Jabbary'),
        StringStruct(u'FileDescription', u'Advanced DNS Configuration Tool'),
        StringStruct(u'FileVersion', u'{app_version}'),
        StringStruct(u'InternalName', u'DNSManagerPro'),
        StringStruct(u'LegalCopyright', u'Copyright (c) 2025 Ali Jabbary'),
        StringStruct(u'OriginalFilename', u'DNSManagerPro.exe'),
        StringStruct(u'ProductName', u'DNS Manager Pro'),
        StringStruct(u'ProductVersion', u'{app_version}'),
        StringStruct(u'Comments', u'https://alijabbary.com')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""

# Write version info to file
Path('version_info.txt').write_text(version_info_content)
