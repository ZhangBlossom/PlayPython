import requests
import time
import random

# 目标URL列表
urls = [
    'https://zhangblossom.blog.csdn.net/article/details/137224076?spm=1001.2014.3001.5502',
    'https://zhangblossom.blog.csdn.net/article/details/137184049?spm=1001.2014.3001.5502',
    'https://zhangblossom.blog.csdn.net/article/details/136355833?spm=1001.2014.3001.5502',
    'https://zhangblossom.blog.csdn.net/article/details/136085994?spm=1001.2014.3001.5502',
    'https://zhangblossom.blog.csdn.net/article/details/135503336?spm=1001.2014.3001.5502',
    'https://zhangblossom.blog.csdn.net/article/details/134354438?spm=1001.2014.3001.5502',
    'https://zhangblossom.blog.csdn.net/article/details/133522946?spm=1001.2014.3001.5502',
    'https://zhangblossom.blog.csdn.net/article/details/140294477?spm=1001.2014.3001.5502',
    'https://zhangblossom.blog.csdn.net/article/details/140136559?spm=1001.2014.3001.5502',
    'https://zhangblossom.blog.csdn.net/article/details/140128893?spm=1001.2014.3001.5502',
    'https://zhangblossom.blog.csdn.net/article/details/139885858?spm=1001.2014.3001.5502',
    'https://zhangblossom.blog.csdn.net/article/details/139885573?spm=1001.2014.3001.5502',
    'https://zhangblossom.blog.csdn.net/article/details/139885354?spm=1001.2014.3001.5502',
    'https://zhangblossom.blog.csdn.net/article/details/139885354?spm=1001.2014.3001.5502',
    'https://zhangblossom.blog.csdn.net/article/details/139504022?spm=1001.2014.3001.5502',
    'https://zhangblossom.blog.csdn.net/article/details/139531517?spm=1001.2014.3001.5502',
    'https://zhangblossom.blog.csdn.net/article/details/139531211?spm=1001.2014.3001.5502',
    'https://zhangblossom.blog.csdn.net/article/details/139507451?spm=1001.2014.3001.5502',
    'https://zhangblossom.blog.csdn.net/article/details/139507371?spm=1001.2014.3001.5502',
    'https://zhangblossom.blog.csdn.net/article/details/139506203?spm=1001.2014.3001.5502',
    'https://zhangblossom.blog.csdn.net/article/details/139506037?spm=1001.2014.3001.5502',
    'https://zhangblossom.blog.csdn.net/article/details/139505881?spm=1001.2014.3001.5502',
    'https://zhangblossom.blog.csdn.net/article/details/139505545?spm=1001.2014.3001.5502',
    'https://zhangblossom.blog.csdn.net/article/details/139505193?spm=1001.2014.3001.5502',
    'https://zhangblossom.blog.csdn.net/article/details/138213527?spm=1001.2014.3001.5502',
    'https://zhangblossom.blog.csdn.net/article/details/138114436?spm=1001.2014.3001.5502',
    'https://zhangblossom.blog.csdn.net/article/details/138114367?spm=1001.2014.3001.5502',
    'https://zhangblossom.blog.csdn.net/article/details/138114270?spm=1001.2014.3001.5502'
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

for attempt in range(max_attempts):
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
        time.sleep(60)  # 休眠时间可以根据需要调整
    except requests.RequestException as e:
        print(f'发生网络异常：{e}，将在60秒后重试')
        time.sleep(60)
