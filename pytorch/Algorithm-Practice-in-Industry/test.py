import os
FEISHU_URL = os.environ.setdefault("FEISHU_URL", "https://open.feishu.cn/open-apis/bot/v2/hook/ee6dbab7-ffc5-4389-8d2f-c56220858720")
FEISHU_URL = os.environ.get("FEISHU_URL", None)
print(FEISHU_URL)