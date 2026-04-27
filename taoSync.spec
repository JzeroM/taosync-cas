# -*- mode: python ; coding: utf-8 -*-

import os
import sys

# 获取项目根目录路径，解决 pathex 问题
project_root = os.path.dirname(os.path.abspath(__file__))

a = Analysis(
    # 1. 入口文件
    ['main.py'],
    
    # 2. 搜索路径：添加项目根目录，确保能找到 common, service 等自定义包
    pathex=[project_root],
    
    # 3. 二进制依赖（如无特殊 C 库，通常为空）
    binaries=[],
    
    # 4. 数据文件：前端静态资源（关键！）
    datas=[
        ('frontend/dist/', 'front'),
        ('logo.ico', '.')  # 可选：如果你希望 exe 内嵌图标
    ],
    
    # 5. 【核心修复】隐藏导入：手动指定 PyInstaller 无法自动分析的自定义模块
    hiddenimports=[
        # Service 层（解决 ImportError: jobClient）
        'service.syncJob.jobClient',
        'service.syncJob.jobService',
        'service.alist.alistClient',
        'service.alist.alistService',
        
        # Mapper 层
        'mapper.jobMapper',
        'mapper.engineMapper',
        'mapper.notifyMapper',
        
        # Common 层
        'common.LNG',
        'common.utils',
        'common.logger',
        'common.security',
        
        # Controller 层
        'controller.jobController',
        'controller.engineController',
        'controller.notifyController',
        'controller.systemController',
        
        # 第三方库（PyInstaller 容易漏扫的动态依赖）
        'apscheduler.schedulers.background',
        'apscheduler.triggers.cron',
        'pathspec',
        'pathspec.patterns.gitwildmatch'
    ],
    
    # 6. 钩子与排除配置
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],  # 可在此排除不需要的库（如调试模块）以减小体积
    
    # 7. 打包选项
    noarchive=False,  # False 表示打包为单文件（或单目录）的压缩形式
    optimize=0,       # 优化级别，0 为不优化（保持调试信息）
)

# 构建 PYZ 归档（包含纯 Python 模块）
pyz = PYZ(a.pure)

# 构建可执行文件 (EXE)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    
    # 选项列表
    [],
    
    # 输出配置
    name='taoSync',          # 生成的可执行文件名称
    debug=False,              # 关闭调试信息
    bootloader_ignore_signals=False,
    strip=False,              # 保留符号信息（False 更稳定）
    upx=True,                 # 启用 UPX 压缩（减小体积）
    upx_exclude=[],          # UPX 排除列表
    
    # 运行时配置
    runtime_tmpdir=None,      # 单文件模式解压的临时目录
    console=True,             # 是否显示控制台窗口（True 便于查看日志）
    disable_windowed_traceback=False,
    argv_emulation=False,
    
    # 系统级配置
    target_arch=None,         # 目标架构（None 为当前系统）
    codesign_identity=None,   # macOS 代码签名（暂无）
    entitlements_file=None,   # macOS 权限文件（暂无）
    
    # 图标（这里设置会覆盖外部图标，确保 logo.ico 文件存在）
    icon=os.path.join(project_root, 'logo.ico')
)

# 如果你需要打包为“文件夹模式”（而非单文件），取消注释以下代码
# coll = COLLECT(
#     exe,
#     a.binaries,
#     a.datas,
#     a.zipfiles,
#     name='taoSync_folder'  # 输出文件夹名称
# )
