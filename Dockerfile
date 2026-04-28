# 构建阶段
FROM python:3.11-slim as builder

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    pkg-config \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用程序源代码
COPY . .

# 创建前端符号链接（方案三核心修复）
RUN ln -snf /app/frontend/dist /app/front

# 运行时阶段
FROM python:3.11-slim

# 设置时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 设置环境变量
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/usr/local/bin:$PATH \
    TAO_PORT=8023 \
    TAO_EXPIRES=2 \
    TAO_LOG_LEVEL=1 \
    TAO_CONSOLE_LEVEL=2 \
    TAO_LOG_SAVE=7 \
    TAO_TASK_SAVE=0 \
    TAO_TASK_TIMEOUT=72

# 安装运行时依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 从构建阶段复制已安装的包
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 复制应用程序代码
COPY --from=builder /app /app

# 确保符号链接存在
RUN ln -snf /app/frontend/dist /app/front

# 创建必要的目录结构
RUN mkdir -p /app/data/logs \
    /app/data/temp \
    /app/data/config

# 设置文件权限
RUN chmod 755 /app/data

# 验证前端文件结构
RUN echo "验证前端文件结构：" && \
    echo "front/index.html 存在: $(if [ -f /app/front/index.html ]; then echo '✅'; else echo '❌'; fi)" && \
    echo "frontend/dist/index.html 存在: $(if [ -f /app/frontend/dist/index.html ]; then echo '✅'; else echo '❌'; fi)"

# 暴露端口
EXPOSE 8023

# 健康检查
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8023/health 2>/dev/null || python -c "import socket; s = socket.socket(); s.connect(('127.0.0.1', 8023))"

# 启动命令
CMD ["python", "main.py"]
