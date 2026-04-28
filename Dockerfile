# 使用作者提供的构建环境
FROM dr34m/tao-sync:not-for-use-pip-req AS builder

WORKDIR /app
COPY . .

# 🔧 关键修复：安装依赖并清理缓存
RUN pip install -r requirements.txt && \
    rm -rf build/ dist/ && \
    pyinstaller --clean taoSync.spec

# 使用作者提供的运行环境
FROM dr34m/tao-sync:not-for-use-alpine

WORKDIR /app

# 🔧 关键修复：复制可执行文件并赋予权限
COPY --from=builder /app/dist/taoSync /app/
RUN chmod +x /app/taoSync

# 挂载数据卷（存放配置和数据库）
VOLUME /app/data

# 设置环境变量（端口、日志等级、时区等）
ENV TAO_PORT=8023 \
    TAO_EXPIRES=2 \
    TAO_LOG_LEVEL=1 \
    TAO_CONSOLE_LEVEL=2 \
    TAO_LOG_SAVE=7 \
    TAO_TASK_SAVE=0 \
    TAO_TASK_TIMEOUT=72 \
    TZ=Asia/Shanghai

EXPOSE 8023

# 🔧 使用绝对路径启动
CMD ["/app/taoSync"]
