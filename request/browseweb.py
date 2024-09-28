import requests
import time
import random

# 目标URL列表
urls = [
    'https://zhangblossom.blog.csdn.net/article/details/137224076?spm=1001.2014.3001.5502',
    'https://blog.csdn.net/Zhangsama1/article/details/141124289?spm=1001.2014.3001.5501'
]

# User-Agent 列表
user_agents = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 '
    'Mobile Safari/537.36',
]

count = 0
max_attempts = 10  # 最大尝试次数

while True:
    try:
        for url in urls:
            # 随机选择一个 User-Agent
            headers = {'User-Agent': random.choice(user_agents)}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                count += 1
                print(f'访问成功 {url}，当前成功次数：{count}')
            else:
                print(f'访问失败 {url}，状态码：{response.status_code}')
        time.sleep(30)  # 休眠时间可以根据需要调整
    except requests.RequestException as e:
        print(f'发生网络异常：{e}，将在60秒后重试')
        time.sleep(30)
