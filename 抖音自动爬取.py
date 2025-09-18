import requests
from DrissionPage import ChromiumPage

# 正确的 ChromiumPage 初始化
page = ChromiumPage()

# 访问抖音用户页面
url = "https://www.douyin.com/user/MS4wLjABAAAAUkp0LFrZx-_dlunt_RPZdq9OKoiZzXwm-C6HB8sZJvc?from_tab_name=main&vid=7523656599115992346"
page.get(url)

print("页面已加载完成")