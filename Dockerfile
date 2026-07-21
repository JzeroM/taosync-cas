FROM python:3.11-slim

# 时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 对齐原版 main.py 里的变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TAO_PORT=8023

WORKDIR /app

# 装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制整个仓库代码
COPY . .

# 原版 main.py 运行时找 ./front
# CI 里 web/dist 是真实产物，这里做软链，不动代码
RUN ln -sfn /app/web/dist /app/front

# 数据持久化目录
RUN mkdir -p /app/data/logs /app/data/temp /app/data/config \
    && chmod -R 755 /app/data

EXPOSE 8023
CMD ["python", "main.py"]
