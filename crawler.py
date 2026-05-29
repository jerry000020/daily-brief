#!/usr/bin/env python3
"""
Playwright 爬虫框架
FB & INS Reels 数据抓取
（注：由于社交平台反爬机制，此框架供学习使用）
"""

import asyncio
import random
from typing import List, Dict
from playwright.async_api import async_playwright, Browser, Page

# 配置
HEADLESS = False  # 显示浏览器窗口，便于调试
WAIT_TIME = 6000  # 等待 6 秒让页面完全加载
SCROLL_TIMES = 2  # 滚动 2 次


class SocialMediaCrawler:
    """社交媒体爬虫基类"""
    
    def __init__(self, platform: str):
        self.platform = platform
        self.browser = None
        self.context = None
        self.page = None
    
    async def __aenter__(self):
        """初始化浏览器"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=HEADLESS)
        self.context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        self.page = await self.context.new_page()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """关闭浏览器"""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
    
    async def scroll_page(self, times: int = SCROLL_TIMES):
        """滚动页面加载更多内容"""
        for i in range(times):
            await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(2)
    
    async def handle_popups(self):
        """处理弹窗和登录提示"""
        try:
            # 等待可能的按钮出现并点击
            buttons = await self.page.query_selector_all("button")
            for button in buttons:
                text = await button.inner_text()
                if any(keyword in text.lower() for keyword in ["accept", "close", "dismiss", "later"]):
                    try:
                        await button.click()
                    except:
                        pass
        except:
            pass
    
    async def extract_data(self) -> List[Dict]:
        """提取数据（子类重写）"""
        raise NotImplementedError
    
    async def crawl(self, url: str) -> List[Dict]:
        """执行爬取"""
        print(f"🚀 正在爬取: {self.platform}")
        await self.page.goto(url)
        
        # 等待页面加载
        await asyncio.sleep(WAIT_TIME / 1000)
        await self.handle_popups()
        
        # 滚动加载更多内容
        await self.scroll_page()
        await asyncio.sleep(2)
        
        # 提取数据
        return await self.extract_data()


class FacebookCrawler(SocialMediaCrawler):
    """Facebook Reels 爬虫"""
    
    def __init__(self):
        super().__init__("Facebook")
    
    async def extract_data(self) -> List[Dict]:
        """提取 Facebook Reels 数据"""
        videos = []
        
        try:
            # 查找视频链接
            links = await self.page.query_selector_all("a[href*='reel'], a[href*='watch']")
            
            for link in links[:5]:  # 只取前5个
                try:
                    href = await link.get_attribute("href")
                    if href and ("reel" in href or "watch" in href):
                        # 查找封面图
                        img = await link.query_selector("img")
                        cover = ""
                        if img:
                            cover = await img.get_attribute("src") or await img.get_attribute("data-src") or ""
                        
                        # 查找标题
                        title_elem = await link.query_selector("h1, h2, h3, h4, h5, h6, span")
                        title = "FB 创意视频"
                        if title_elem:
                            title = await title_elem.inner_text()
                            if len(title) > 50:
                                title = title[:50] + "..."
                        
                        videos.append({
                            "platform": "FB",
                            "url": href if href.startswith("http") else f"https://www.facebook.com{href}",
                            "title": title,
                            "cover": cover,
                            "time": "近24小时",
                            "description": "精彩创意内容"
                        })
                except Exception as e:
                    print(f"   提取失败: {e}")
                    continue
                    
        except Exception as e:
            print(f"   提取数据出错: {e}")
        
        return videos


class InstagramCrawler(SocialMediaCrawler):
    """Instagram Reels 爬虫"""
    
    def __init__(self):
        super().__init__("Instagram")
    
    async def extract_data(self) -> List[Dict]:
        """提取 Instagram Reels 数据"""
        videos = []
        
        try:
            # 查找视频链接
            links = await self.page.query_selector_all("a[href*='reel']")
            
            for link in links[:5]:  # 只取前5个
                try:
                    href = await link.get_attribute("href")
                    if href and "reel" in href:
                        # 查找封面图
                        img = await link.query_selector("img")
                        cover = ""
                        if img:
                            cover = await img.get_attribute("src") or await img.get_attribute("data-src") or ""
                        
                        # 查找标题
                        title_elem = await link.query_selector("h1, h2, h3, h4, h5, h6, span")
                        title = "INS 创意视频"
                        if title_elem:
                            title = await title_elem.inner_text()
                            if len(title) > 50:
                                title = title[:50] + "..."
                        
                        videos.append({
                            "platform": "INS",
                            "url": href if href.startswith("http") else f"https://www.instagram.com{href}",
                            "title": title,
                            "cover": cover,
                            "time": "近24小时",
                            "description": "精彩创意内容"
                        })
                except Exception as e:
                    print(f"   提取失败: {e}")
                    continue
                    
        except Exception as e:
            print(f"   提取数据出错: {e}")
        
        return videos


async def main():
    """测试爬虫"""
    print("=" * 60)
    print("🔍 Playwright 爬虫框架")
    print("=" * 60)
    
    print("\n⚠️  注意：")
    print("   由于社交平台反爬机制，真实爬取需要：")
    print("   1. 配置代理 IP")
    print("   2. 使用真实账户登录")
    print("   3. 遵守平台服务条款")
    print("\n💡 建议使用 main.py 中的模拟数据生成器")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
