# -*- mode: python ; coding: utf-8 -*-
import os
import sys

# 动态获取项目根目录（兼容 CI）
base_path = os.getcwd()

a = Analysis(
    ['main.py'],
    pathex=[base_path],
    binaries=[],
    # 前端资源 + 语言包
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
        'charset_normalizer',  # 显式声明，避免自动收集出错
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
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(base_path, 'logo.ico') if os.path.exists(os.path.join(base_path, 'logo.ico')) else None,
)
