# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['c:\\Users\\ELITEBOOK 840 G3\\Desktop\\local LLM chat\\backend\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('.env', '.')],
    hiddenimports=['uvicorn.logging', 'uvicorn.protocols', 'uvicorn.lifespan', 'uvicorn.protocols.http', 'uvicorn.protocols.http.auto', 'uvicorn.protocols.websockets', 'uvicorn.protocols.websockets.auto'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
