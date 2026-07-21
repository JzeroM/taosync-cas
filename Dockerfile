FROM python:3.11-slim

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 对齐 main.py 里找的 ./front
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TAO_PORT=8023

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# CI 里前端产物在 web/dist，直接软链给 main.py 认的 front/
RUN ln -sfn /app/web/dist /app/front

RUN mkdir -p /app/data/logs /app/data/temp /app/data/config \
    && chmod -R 755 /app/data

EXPOSE 8023
CMD ["python", "main.py"]
