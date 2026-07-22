# -*- mode: python ; coding: utf-8 -*-
import os

base_path = os.getcwd()

a = Analysis(
    ['main.py'],
    pathex=[base_path],
    binaries=[],
    datas=[
        (os.path.join(base_path, 'front'), 'front'),
        (os.path.join(base_path, 'locales'), 'locales'),
    ],
    hiddenimports=[
        'tornado',
        'controller.systemController',
        'controller.jobController',
        'controller.notifyController',
        'service.system',
        'service.syncJob.jobClient',
        'mapper.jobMapper',
        'common.config',
        'common.LNG',
        'charset_normalizer',   # 声明导入，不走子进程钩子
    ],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    name='taoSync',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(base_path, 'logo.ico') if os.path.exists(os.path.join(base_path, 'logo.ico')) else None,
)

# 目录模式：不触发单文件解压，彻底解决 WinError 1455
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    a.zipfiles,
    name='taoSync',
)
