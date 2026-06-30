# calculator.spec
# PyInstaller spec file for Windows executable

block_cipher = None

a = Analysis(
    ['calculator.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
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

# For Windows: create a single executable
exec_options = [
    '--onefile',
    '--name=calculator-win',
    '--windowed',
    '--icon=calculator.ico',
    '--add-data=calculator.ico;.',
]

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [('v', None, 'OPTION')],
    name='calculator-win',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='calculator.ico',
)
