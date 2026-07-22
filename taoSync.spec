# taoSync.spec
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
        'charset_normalizer',
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
    console=True,
    upx=True,
    icon=os.path.join(base_path, 'logo.ico') if os.path.exists(os.path.join(base_path, 'logo.ico')) else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    a.zipfiles,
    name='taoSync',
)
