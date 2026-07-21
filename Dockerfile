FROM python:3.11-slim

# ===== 基础环境 =====
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# ===== 业务环境变量 =====
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TAO_PORT=8023 \
    TAO_EXPIRES=2 \
    TAO_LOG_LEVEL=1 \
    TAO_CONSOLE_LEVEL=2 \
    TAO_LOG_SAVE=7 \
    TAO_TASK_SAVE=0 \
    TAO_TASK_TIMEOUT=72

# ===== 运行时依赖 =====
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ===== 安装 Python 依赖 =====
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ===== 复制代码 & 前端 =====
# 注意：CI 里会把 dist 对齐成 front/ 目录喂进来
COPY . .

# ===== 数据目录 =====
RUN mkdir -p /app/data/logs /app/data/temp /app/data/config \
    && chmod -R 755 /app/data

# ===== 健康检查 =====
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD curl -fs http://localhost:${TAO_PORT}/ || exit 1

EXPOSE 8023

CMD ["python", "main.py"]
