# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_all

# 动态拿 spec 所在目录
base_path = os.path.abspath(os.path.dirname(__file__))

# charset_normalizer 兼容
charset_datas, charset_binaries, charset_hiddenimports = collect_all('charset_normalizer')

a = Analysis(
    ['main.py'],
    pathex=[base_path],
    binaries=charset_binaries,
    datas=[
        # CI 里前端产物在 front/，打进 exe 内部也叫 front/
        (os.path.join(base_path, 'front'), 'front'),
        (os.path.join(base_path, 'locales'), 'locales'),
    ] + charset_datas,
    hiddenimports=charset_hiddenimports,
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
    name='taoSync',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # 有就引，没有就不挂
    icon=os.path.join(base_path, 'logo.ico') if os.path.exists(os.path.join(base_path, 'logo.ico')) else None,
)
