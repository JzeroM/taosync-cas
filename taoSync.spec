# -*- mode: python ; coding: utf-8 -*-
import os

# 本地开发时 web/dist 构建完，CI 里会提前拷到 web/dist
a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    # 关键：web/dist 里的所有东西，运行时放进 front/ 里
    datas=[('web/dist', 'front')],
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
    ],
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
    console=True,
    icon='logo.ico' if os.path.exists('logo.ico') else None,
)
