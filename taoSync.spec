# -*- mode: python ; coding: utf-8 -*-

import os
import sys

# 🔧 修复：使用 getcwd() 替代 __file__，解决 Docker 构建环境报错
project_root = os.getcwd()

# 添加项目根目录到 Python 路径，确保 PyInstaller 能搜索到自定义包
sys.path.insert(0, project_root)

block_cipher = None

a = Analysis(
    # 1. 主入口文件
    ['main.py'],
    
    # 2. 搜索路径：关键！指向项目根目录，解决 ModuleNotFoundError
    pathex=[project_root],
    
    # 3. 二进制依赖（如无特殊 C 库，通常为空）
    binaries=[],
    
    # 4. 数据文件：前端静态资源（Vue 编译后的 dist 目录）
    datas=[
        ('frontend/dist', 'frontend/dist'),
        ('logo.ico', '.'),
        ('data', 'data')  # 包含配置文件、数据库等
    ],
    
    # 5. 【核心】隐藏导入：显式声明所有自定义模块，防止打包遗漏
    hiddenimports=[
        # Service 层（解决 jobClient 等导入错误）
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
    
    # 6. 其他配置
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],  # 可在此排除不需要的库以减小体积
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False  # False 表示打包为压缩形式
)

# 构建 PYZ 归档（包含纯 Python 模块）
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

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
    upx_exclude=[],
    
    # 运行时配置
    runtime_tmpdir=None,      # 单文件模式解压的临时目录
    console=True,             # 是否显示控制台窗口（True 便于查看日志）
    disable_windowed_traceback=False,
    argv_emulation=False,
    
    # 系统级配置
    target_arch=None,         # 目标架构（None 为当前系统）
    codesign_identity=None,   # macOS 代码签名（暂无）
    entitlements_file=None,   # macOS 权限文件（暂无）
    
    # 图标配置（确保 logo.ico 文件存在）
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
