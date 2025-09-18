#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音评论爬虫和音频提取示例
注意：此代码仅作为示例，实际使用时需要考虑以下问题：
1. 抖音的反爬虫措施会阻止频繁的请求
2. 需要处理登录状态和cookies
3. 页面结构可能会变化，选择器需要相应更新
4. 请遵守网站使用条款和相关法律法规
"""

import time
import json
import random
import requests
import re
import os
from urllib.parse import urlencode
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

class DouyinCommentCrawler:
    def __init__(self, email=None, password=None):
        self.ua = UserAgent()
        self.headers = {
            'User-Agent': self.ua.random,
            'Referer': 'https://www.douyin.com/',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': ''  # 登录后会自动填充
        }
        self.email = email
        self.password = password
        self.cookies = {}
        self.driver = None
        
    def check_chrome_installation(self):
        """
        检查 Edge 或 Chrome 浏览器是否已安装
        :return: (browser_type, is_available)
        """
        import platform
        system = platform.system()
        
        if system == "Darwin":  # macOS
            edge_paths = [
                "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
            ]
            chrome_paths = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Chromium.app/Contents/MacOS/Chromium"
            ]
        elif system == "Linux":
            edge_paths = [
                "/usr/bin/microsoft-edge",
                "/usr/bin/microsoft-edge-stable"
            ]
            chrome_paths = [
                "/usr/bin/google-chrome",
                "/usr/bin/chromium-browser",
                "/usr/bin/chromium"
            ]
        else:  # Windows
            edge_paths = [
                "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
                "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe"
            ]
            chrome_paths = [
                "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
            ]
        
        # 优先检查 Edge
        for path in edge_paths:
            if os.path.exists(path):
                return ("edge", True)
                
        # 然后检查 Chrome
        for path in chrome_paths:
            if os.path.exists(path):
                return ("chrome", True)
                
        return ("none", False)
        
    def extract_video_id(self, short_url):
        """
        从抖音短链接中提取视频ID
        :param short_url: 抖音短链接
        :return: 视频ID
        """
        try:
            # 设置请求头，模拟浏览器访问
            headers = {'User-Agent': self.ua.random}
            
            # 发送GET请求，获取重定向后的URL
            response = requests.get(short_url, headers=headers, allow_redirects=True)
            final_url = response.url
            
            # 从最终URL中提取视频ID
            # 示例：https://www.douyin.com/video/7123456789012345678
            video_id_match = re.search(r'/video/(\d+)', final_url)
            if video_id_match:
                return video_id_match.group(1)
                
            # 有时URL格式可能不同，尝试其他匹配方式
            video_id_match = re.search(r'item_ids=(\d+)', final_url)
            if video_id_match:
                return video_id_match.group(1)
                
            print(f"无法从URL提取视频ID: {final_url}")
            return None
        except Exception as e:
            print(f"提取视频ID时出错: {e}")
            return None
    
    def login(self, email, password):
        """
        使用邮箱和密码登录抖音
        :param email: 邮箱
        :param password: 密码
        :return: 是否登录成功
        """
        try:
            # 初始化Chrome浏览器
            chrome_options = ChromeOptions()
            chrome_options.add_argument('--headless')  # 无头模式，不显示浏览器窗口
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument(f'user-agent={self.ua.random}')
            
            # 自动管理 ChromeDriver
            service = ChromeService(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.get('https://www.douyin.com/')
            
            # 等待登录按钮加载
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), '登录')]"))
            )
            
            # 点击登录按钮
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '登录')]")
            login_button.click()
            
            # 等待邮箱登录选项
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), '邮箱登录')]"))
            )
            
            # 点击邮箱登录
            email_login = self.driver.find_element(By.XPATH, "//div[contains(text(), '邮箱登录')]")
            email_login.click()
            
            # 输入邮箱和密码
            email_input = self.driver.find_element(By.XPATH, "//input[@placeholder='请输入邮箱']")
            email_input.send_keys(email)
            
            password_input = self.driver.find_element(By.XPATH, "//input[@placeholder='请输入密码']")
            password_input.send_keys(password)
            
            # 点击登录
            submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()
            
            # 等待登录成功
            time.sleep(5)
            
            # 获取cookies
            cookies = self.driver.get_cookies()
            cookie_str = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
            self.headers['Cookie'] = cookie_str
            
            print("登录成功，已获取cookies")
            return True
            
        except Exception as e:
            print(f"登录失败: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
        
    def get_comments(self, video_id, cursor=0, count=20):
        """
        获取指定视频的评论
        :param video_id: 视频ID
        :param cursor: 分页游标
        :param count: 每页评论数量
        :return: 评论列表
        """
        # 这是一个模拟的API URL，实际URL可能不同
        api_url = "https://www.douyin.com/aweme/v1/web/comment/list/"
        
        params = {
            'aweme_id': video_id,
            'cursor': cursor,
            'count': count,
            'device_platform': 'webapp',
            'aid': '6383',
        }
        
        try:
            # 添加随机延迟，避免频繁请求
            time.sleep(random.uniform(1, 3))
            
            url = f"{api_url}?{urlencode(params)}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                comments = data.get('comments', [])
                has_more = data.get('has_more', 0)
                next_cursor = data.get('cursor', 0)
                
                return {
                    'comments': comments,
                    'has_more': has_more,
                    'next_cursor': next_cursor
                }
            else:
                print(f"请求失败，状态码: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"获取评论时出错: {e}")
            return None
    
    def parse_comments(self, comments_data):
        """
        解析评论数据
        :param comments_data: API返回的评论数据
        :return: 格式化后的评论列表
        """
        if not comments_data or 'comments' not in comments_data:
            return []
            
        parsed_comments = []
        
        for comment in comments_data['comments']:
            try:
                comment_info = {
                    'cid': comment.get('cid', ''),
                    'text': comment.get('text', ''),
                    'create_time': comment.get('create_time', 0),
                    'digg_count': comment.get('digg_count', 0),  # 点赞数
                    'user': {
                        'uid': comment.get('user', {}).get('uid', ''),
                        'nickname': comment.get('user', {}).get('nickname', ''),
                        'avatar': comment.get('user', {}).get('avatar_thumb', {}).get('url_list', [''])[0]
                    },
                    'reply_comment_total': comment.get('reply_comment_total', 0)  # 回复数
                }
                parsed_comments.append(comment_info)
            except Exception as e:
                print(f"解析评论时出错: {e}")
                continue
                
        return parsed_comments
        
    def crawl_all_comments(self, video_id, max_pages=5):
        """
        爬取指定视频的所有评论（最多爬取指定页数）
        :param video_id: 视频ID
        :param max_pages: 最大爬取页数
        :return: 所有评论列表
        """
        all_comments = []
        cursor = 0
        page = 0
        
        while page < max_pages:
            print(f"正在爬取第 {page+1} 页评论...")
            result = self.get_comments(video_id, cursor)
            
            if not result:
                break
                
            comments = self.parse_comments(result)
            all_comments.extend(comments)
            
            has_more = result.get('has_more', 0)
            if not has_more:
                break
                
            cursor = result.get('next_cursor', 0)
            page += 1
            
        return all_comments
        
    def save_comments(self, comments, output_file):
        """
        保存评论到文件
        :param comments: 评论列表
        :param output_file: 输出文件路径
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(comments, f, ensure_ascii=False, indent=4)
        print(f"已保存 {len(comments)} 条评论到 {output_file}")
        
    def extract_audio_url(self, video_id):
        """
        使用 requests 直接提取视频的音频链接
        :param video_id: 视频ID
        :return: 音频URL
        """
        try:
            # 尝试直接通过API获取视频信息
            api_urls = [
                f"https://www.douyin.com/aweme/v1/web/aweme/detail/?aweme_id={video_id}",
                f"https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={video_id}",
            ]
            
            for api_url in api_urls:
                try:
                    print(f"正在尝试API: {api_url}")
                    response = requests.get(api_url, headers=self.headers, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # 解析不同API返回的数据结构
                        if 'aweme_detail' in data:
                            video_info = data['aweme_detail']
                        elif 'item_list' in data and data['item_list']:
                            video_info = data['item_list'][0]
                        else:
                            continue
                            
                        # 查找音频或视频URL
                        if 'music' in video_info:
                            music_info = video_info['music']
                            if 'play_url' in music_info:
                                audio_url = music_info['play_url']['url_list'][0]
                                print(f"找到音频链接: {audio_url}")
                                return audio_url
                                
                        # 如果没有单独的音频，尝试从视频中提取
                        if 'video' in video_info:
                            video_info_detail = video_info['video']
                            if 'play_addr' in video_info_detail:
                                video_url = video_info_detail['play_addr']['url_list'][0]
                                print(f"找到视频链接: {video_url}")
                                return video_url
                                
                except Exception as e:
                    print(f"API请求失败: {e}")
                    continue
            
            print("所有API尝试失败，使用备用方法...")
            # 备用方法：尝试构建可能的音频URL
            possible_urls = [
                f"https://sf-tk-sg.ibytedtos.com/obj/ies-music-sg/{video_id}.mp3",
                f"https://sf1-cdn-tos.douyinstatic.com/obj/ies-music/{video_id}.mp3",
                f"https://sf6-cdn-tos.douyinstatic.com/obj/ies-music/{video_id}.mp3",
            ]
            
            for url in possible_urls:
                try:
                    head_response = requests.head(url, headers=self.headers, timeout=5)
                    if head_response.status_code == 200:
                        print(f"找到可用的音频链接: {url}")
                        return url
                except:
                    continue
            
            print("无法找到音频链接")
            return None
            
        except Exception as e:
            print(f"提取音频链接时出错: {e}")
            return None
        
    def download_audio(self, url, output_path):
        """
        下载音频文件
        :param url: 音频URL
        :param output_path: 输出文件路径
        :return: 是否下载成功
        """
        try:
            # 发送请求获取音频内容
            response = requests.get(url, headers=self.headers, stream=True)
            
            if response.status_code == 200:
                # 确保输出目录存在
                os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
                
                # 写入文件
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            
                print(f"音频已下载到: {output_path}")
                return True
            else:
                print(f"下载失败，状态码: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"下载音频时出错: {e}")
            return False
    
    def extract_and_download_audio(self, video_id, output_dir='.'):
        """
        提取并下载视频的音频
        :param video_id: 视频ID
        :param output_dir: 输出目录
        :return: 下载的文件路径或None
        """
        try:
            # 获取音频URL
            audio_url = self.extract_audio_url(video_id)
            
            if not audio_url:
                print("无法获取音频URL")
                return None
                
            # 设置输出文件路径
            output_path = os.path.join(output_dir, f'douyin_audio_{video_id}.mp3')
            
            # 下载音频
            if self.download_audio(audio_url, output_path):
                return output_path
            
            return None
            
        except Exception as e:
            print(f"提取和下载音频时出错: {e}")
            return None

def main():
    # 实例化爬虫对象
    crawler = DouyinCommentCrawler()
    
    # 使用新的抖音链接
    short_url = "https://v.douyin.com/Utl72nAPORE/"
    
    print("开始测试抖音音频爬取...")
    print("🔄 使用纯 API 方式，无需浏览器")
    print(f"目标链接: {short_url}")
    
    # 提取视频ID
    video_id = crawler.extract_video_id(short_url)
    if not video_id:
        print("无法获取视频ID，退出程序")
        return
    
    print(f"成功提取视频ID: {video_id}")
    
    # 仅提取并下载音频
    print("开始提取并下载音频...")
    audio_path = crawler.extract_and_download_audio(video_id, output_dir='audio')
    if audio_path:
        print(f"🎵 音频已成功下载到: {audio_path}")
        print("✅ 测试完成！")
    else:
        print("❌ 音频提取或下载失败")
        print("💡 建议：抖音可能更新了API或增加了反爬虫措施")
    
    # 不再需要关闭浏览器，因为没有使用浏览器

if __name__ == "__main__":
    main()
