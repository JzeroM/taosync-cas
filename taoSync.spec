# -*- mode: python ; coding: utf-8 -*-
import os

a = Analysis(
    ['main.py'],
    pathex=['.'],               # 让 controller/service/mapper 都能被正确追踪
    binaries=[],
    # 你的前端在根目录构建，dist/ 映射成运行时的 front/
    datas=[('dist', 'front')],
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
    a.binaries.to_pyz_data(),
    a.zipfiles,
    a.datas,
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
    # 没有 logo.ico 也不报错
    icon='logo.ico' if os.path.exists('logo.ico') else None,
)
