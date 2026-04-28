# 构建阶段
FROM python:3.11-slim as builder

# 设置工作目录
WORKDIR /app

# 安装系统依赖（如果需要编译某些包）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖到用户目录
RUN pip install --user --no-cache-dir -r requirements.txt

# 复制源代码
COPY . .

# 运行时阶段
FROM python:3.11-slim

# 设置环境变量
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PATH=/root/.local/bin:$PATH

# 设置工作目录
WORKDIR /app

# 从构建阶段复制已安装的包
COPY --from=builder /root/.local /root/.local

# 复制应用程序代码
COPY --from=builder /app /app

# 创建必要的目录结构
RUN mkdir -p /app/data/logs \
    /app/data/temp \
    /app/data/config

# 创建非 root 用户
RUN groupadd -r taosync && useradd -r -g taosync -u 1000 taosync \
    && chown -R taosync:taosync /app

# 设置文件权限
RUN chmod 755 /app \
    && chmod 644 /app/*.py 2>/dev/null || true

# 切换到非 root 用户
USER taosync

# 暴露端口（根据你的 config.ini 配置）
EXPOSE 8023

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import socket; s = socket.socket(); s.connect(('127.0.0.1', 8023))" 2>/dev/null || exit 1

# 启动命令
CMD ["python", "main.py"]
