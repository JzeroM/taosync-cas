TaoSync-CAS

<div align="center">

<a href=""><img width="200px" alt="logo" src="frontend/public/logo-200-64.png"/></a>

TaoSync-CAS 是一个魔改自 TaoSync 的自动化同步工具

</div>

✨ 项目特色

TaoSync-CAS​ 是在原版 TaoSync 基础上深度魔改的版本，专门设计用于配合魔改的OpenList，实现自动化的视频文件同步 + CAS文件生成工作流。

🎯 核心功能

无重复同步：解决因魔改openlist删除原视频文件而导致重复同步的问题

🎯 相关项目
1. TaoSync-CAS (本项目)

地址: https://github.com/JzeroM/taosync-cas

功能: 基于文件名前缀匹配的智能同步工具

2. OpenList-CAS (配套项目)

地址: https://github.com/GitYuA/OpenList-CAS

功能: 视频文件到CAS文件的自动化转换工具

🔄 协同工作流程
TaoSync-CAS → 同步视频文件 → OpenList-CAS → 生成.cas文件 → TaoSync-CAS (跳过已处理文件)
🚀 快速开始
🐳 Docker 部署

TaoSync-CAS 提供两种镜像源，你可以根据需要选择：

方案一：使用 Docker Hub 镜像 (推荐)
```sh
docker run -d \
  --restart=always \
  -p 8023:8023 \
  -v /path/to/data:/app/data \
  --name=taosync-cas \
  miuior/taosync-cas:v1.1.1
```  
方案二：使用 GitHub Container Registry 镜像
```sh
docker run -d \
  --restart=always \
  -p 8023:8023 \
  -v /path/to/data:/app/data \
  --name=taosync-cas \
  ghcr.io/jzerom/taosync-cas:latest
```
🐳 Docker Compose 部署
方案一：使用 Docker Compose 配合 Docker Hub

创建 docker-compose.yml文件：
```sh
yaml
version: '3.8'

services:
  taosync:
    image: miuior/taosync-cas:v1.1.1
    container_name: taosync_cas
    restart: always
    ports:
      - "8023:8023"
    volumes:
      - ./data:/app/data
    environment:
      - TZ=Asia/Shanghai
```
方案二：使用 Docker Compose 配合 GitHub Container Registry
```sh
version: '3.8'

services:
  taosync:
    image: ghcr.io/jzerom/taosync-cas:latest
    container_name: taosync_cas
    restart: always
    ports:
      - "8023:8023"
    volumes:
      - ./data:/app/data
    environment:
      - TZ=Asia/Shanghai
```
启动和停止

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

🔐 获取初始密码

# 查看容器日志获取随机生成的密码
```sh
docker logs taosync_cas | grep "Password for admin"
```
# 或查看挂载目录的日志文件
```sh
cat ./data/log/sys_*.log | grep "Password for admin"
```
默认用户名: admin

初始密码: 随机生成，查看日志获取

登录地址: http://localhost:8023

⚠️ 重要：登录后请立即前往系统设置修改密码！

⚠️ 重要说明

[!IMPORTANT]

使用本工具前你必须了解并且会使用魔改的OpenList，本工具没有集成魔改OpenList，你需要额外启动魔改OpenList服务。

🔄 开发状态

开发状态: 持续维护

原项目: 基于 dr34m-cn/taosync
魔改

许可证: AGPL-3.0

📈 Star趋势

https://starchart.cc/JzeroM/taosync-cas.svg?variant=adaptive

📄 许可证

本项目采用 AGPL-3.0 许可证。详见 LICENSE
文件。

🙏 致谢

感谢原项目 dr34m-cn/taosync
提供的基础框架

感谢魔改OpenList项目的开发者

感谢所有贡献者和使用者

🤝 贡献

欢迎提交 Issue 和 Pull Request！

Fork 本仓库

创建功能分支 (git checkout -b feature/AmazingFeature)

提交更改 (git commit -m 'Add some AmazingFeature')

推送到分支 (git push origin feature/AmazingFeature)

开启 Pull Request

📧 联系

GitHub: JzeroM

项目地址: taosync-cas

Docker Hub: miuior/taosync-cas

GitHub Container Registry: ghcr.io/jzerom/taosync-cas
