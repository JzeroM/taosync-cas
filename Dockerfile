FROM python:3.11-slim

# ... 保留其他配置 ...

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

# 设置文件权限（确保 data 目录可写）
RUN chmod 755 /app/data

# 暴露端口
EXPOSE 8023

# 启动命令（使用 root 用户）
CMD ["python", "main.py"]
