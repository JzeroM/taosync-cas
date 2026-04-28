# 第一阶段：构建阶段 (针对 macOS)
FROM dr34m/tao-sync:not-for-use-pip-req AS builder

WORKDIR /app
COPY . .

# 🔧 关键修复：安装依赖并清理缓存
# 🔧 关键修复：创建 PyInstaller 打包时需要的 data 目录
RUN pip install -r requirements.txt && \
    rm -rf build/ dist/ && \
    mkdir -p /app/data && \
    pyinstaller --clean taoSync.spec

# 第二阶段：运行阶段 (Alpine Linux)
FROM dr34m/tao-sync:not-for-use-alpine

WORKDIR /app

# 🔧 可选修复：添加 Alpine Linux 运行环境依赖
RUN apk add --no-cache libstdc++ musl-dev

# 从构建阶段复制可执行文件
COPY --from=builder /app/dist/taoSync /app/

# 🔧 关键修复：确保可执行文件有运行权限
RUN chmod +x /app/taoSync

# 声明数据卷
VOLUME /app/data

# 设置环境变量
ENV TAO_PORT=8023 \
    TAO_EXPIRES=2 \
    TAO_LOG_LEVEL=1 \
    TAO_CONSOLE_LEVEL=2 \
    TAO_LOG_SAVE=7 \
    TAO_TASK_SAVE=0 \
    TAO_TASK_TIMEOUT=72 \
    TZ=Asia/Shanghai \
    PYTHONPATH=/app

EXPOSE 8023

# 🔧 关键修复4：使用绝对路径启动
CMD ["/app/taoSync"]
