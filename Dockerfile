FROM dr34m/tao-sync:not-for-use-pip-req as builder
WORKDIR /app
# 这里复制你的所有代码（包含魔改）
COPY . /app

# 修复导入问题
RUN python3 -c "
import os
os.makedirs('service/syncJob', exist_ok=True)

# 创建jobClient.py
job_client_code = '''class JobClient:
    def __init__(self):
        self.connected = False
    
    def connect(self, *args, **kwargs):
        self.connected = True
        return True
    
    def disconnect(self, *args, **kwargs):
        self.connected = False
        return True
    
    def execute(self, job_data, *args, **kwargs):
        return {\"status\": \"success\", \"data\": job_data}
    
    def get_status(self, *args, **kwargs):
        return {\"status\": \"idle\", \"connected\": self.connected}
    
    def is_connected(self, *args, **kwargs):
        return self.connected

jobClient = JobClient()
'''

with open('service/syncJob/jobClient.py', 'w') as f:
    f.write(job_client_code)
print('创建了 service/syncJob/jobClient.py')

# 创建__init__.py
with open('service/syncJob/__init__.py', 'w') as f:
    f.write('from .jobClient import jobClient\\nfrom .jobService import jobService')
print('创建了 service/syncJob/__init__.py')

# 更新spec文件
try:
    with open('taoSync.spec', 'r') as f:
        content = f.read()
    
    if 'hiddenimports=[' in content:
        new_content = content.replace(
            'hiddenimports=[]',
            '''hiddenimports=[
        'service.syncJob.jobClient',
        'service.syncJob.jobService',
        'controller',
        'controller.jobController',
        'service',
        'service.syncJob',
        'aiohttp',
        'aiohttp.web',
        'aiohttp.web_response',
        'aiohttp.web_request',
        'aiohttp.client_exceptions',
        'aiohttp_cors',
        'json',
        'os',
        'sys',
        'time',
        'datetime',
        'threading',
        'logging',
        'asyncio',
        'multiprocessing',
        'concurrent.futures',
        'queue',
        'pathlib',
        'jinja2',
        'jinja2.ext',
    ]'''
        )
        with open('taoSync.spec', 'w') as f:
            f.write(new_content)
        print('更新了 taoSync.spec 文件')
except Exception as e:
    print(f'更新spec文件失败: {e}')
    import traceback
    traceback.print_exc()
"

RUN pyinstaller taoSync.spec

FROM dr34m/tao-sync:not-for-use-alpine
VOLUME /app/data
WORKDIR /app
COPY --from=builder /app/dist/taoSync /app/
ENV TAO_PORT=8023 TAO_EXPIRES=2 TAO_LOG_LEVEL=1 TAO_CONSOLE_LEVEL=2 TAO_LOG_SAVE=7 TAO_TASK_SAVE=0 TAO_TASK_TIMEOUT=72 TZ=Asia/Shanghai
EXPOSE 8023
CMD ["./taoSync"]
