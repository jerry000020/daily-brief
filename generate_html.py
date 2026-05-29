#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成高质量卡片风网页
"""

import json
from datetime import datetime

def generate_html():
    # 读取数据
    with open('/workspace/每日简报-完整版/data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 生成 HTML
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>海外创意·AI视频·舞台设备 每日简报</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
            color: #1D2129;
            line-height: 1.6;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}

        header {{
            background: linear-gradient(135deg, #165DFF 0%, #4080FF 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(22, 93, 255, 0.25);
            position: relative;
            overflow: hidden;
        }}

        header::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: pulse 8s ease-in-out infinite;
        }}

        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); opacity: 0.5; }}
            50% {{ transform: scale(1.1); opacity: 0.8; }}
        }}

        header h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 10px;
            letter-spacing: 2px;
            position: relative;
            z-index: 1;
        }}

        header .date {{
            font-size: 1.2rem;
            opacity: 0.95;
            font-weight: 400;
            position: relative;
            z-index: 1;
        }}

        header::after {{
            content: '';
            display: block;
            width: 60px;
            height: 4px;
            background: #FF7D00;
            margin: 20px auto 0;
            border-radius: 2px;
            position: relative;
            z-index: 1;
        }}

        main {{
            padding: 50px 0;
        }}

        .section {{
            margin-bottom: 60px;
        }}

        .section-title {{
            background: linear-gradient(90deg, #165DFF 0%, #4080FF 100%);
            color: white;
            padding: 20px 28px;
            font-size: 1.5rem;
            font-weight: 700;
            border-radius: 12px;
            margin-bottom: 32px;
            display: flex;
            align-items: center;
            gap: 12px;
            box-shadow: 0 4px 16px rgba(22, 93, 255, 0.2);
        }}

        .section-title .emoji {{
            font-size: 1.8rem;
        }}

        .cards {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 28px;
        }}

        .card {{
            background: white;
            border-radius: 16px;
            padding: 28px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid rgba(22, 93, 255, 0.08);
            position: relative;
            overflow: hidden;
        }}

        .card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #165DFF 0%, #FF7D00 100%);
            opacity: 0;
            transition: opacity 0.3s ease;
        }}

        .card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 12px 40px rgba(22, 93, 255, 0.18);
        }}

        .card:hover::before {{
            opacity: 1;
        }}

        .card-title {{
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 12px;
            color: #1D2129;
            line-height: 1.4;
        }}

        .card-title .highlight {{
            color: #FF7D00;
        }}

        .card-meta {{
            font-size: 0.85rem;
            color: #86909C;
            margin-bottom: 18px;
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }}

        .card-meta .platform {{
            background: linear-gradient(135deg, #f0f7ff 0%, #e6f0ff 100%);
            color: #165DFF;
            padding: 6px 14px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.8rem;
        }}

        .card-image {{
            width: 100%;
            height: 220px;
            object-fit: cover;
            border-radius: 12px;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        }}

        .card-content {{
            font-size: 0.95rem;
            color: #4B5563;
            margin-bottom: 20px;
            line-height: 1.7;
        }}

        .card-link {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: #165DFF;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.2s ease;
        }}

        .card-link:hover {{
            color: #FF7D00;
            gap: 12px;
        }}

        .card-link::after {{
            content: '→';
            font-size: 1.1rem;
            font-weight: bold;
        }}

        footer {{
            text-align: center;
            padding: 50px 20px;
            color: #86909C;
            font-size: 0.9rem;
            border-top: 1px solid rgba(22, 93, 255, 0.1);
            background: white;
            margin-top: 60px;
        }}

        footer .update-time {{
            margin-bottom: 10px;
            font-weight: 500;
            color: #4B5563;
        }}

        @media (max-width: 768px) {{
            header {{
                padding: 32px 16px;
            }}

            header h1 {{
                font-size: 1.8rem;
            }}

            .section-title {{
                font-size: 1.25rem;
                padding: 16px 20px;
            }}

            .cards {{
                grid-template-columns: 1fr;
                gap: 20px;
            }}

            .card {{
                padding: 22px;
            }}

            .card-image {{
                height: 200px;
            }}
        }}

        @media (max-width: 480px) {{
            header h1 {{
                font-size: 1.5rem;
                letter-spacing: 1px;
            }}

            .section-title {{
                font-size: 1.1rem;
            }}

            .card-title {{
                font-size: 1.1rem;
            }}
        }}

        @media (min-width: 1024px) {{
            .cards {{
                grid-template-columns: repeat(3, 1fr);
            }}
        }}

        .info-tag {{
            display: inline-block;
            background: linear-gradient(135deg, #FF7D00 0%, #ff9500 100%);
            color: white;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-bottom: 14px;
        }}

        .feature-list {{
            list-style: none;
            padding: 0;
            margin: 16px 0;
        }}

        .feature-list li {{
            position: relative;
            padding-left: 24px;
            margin-bottom: 10px;
            font-size: 0.9rem;
            color: #4B5563;
        }}

        .feature-list li::before {{
            content: '✓';
            position: absolute;
            left: 0;
            color: #165DFF;
            font-weight: bold;
            font-size: 1rem;
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>🌐 海外创意·AI视频·舞台设备 每日简报</h1>
            <div class="date">{datetime.now().strftime('%Y年%m月%d日 %A')}</div>
        </div>
    </header>

    <main class="container">
        <section class="section">
            <div class="section-title">
                <span class="emoji">🔥</span>
                <span>FB & INS 创意视频</span>
            </div>
            <div class="cards" id="socialMediaCards">
                {generate_social_cards(data['social_media'])}
            </div>
        </section>

        <section class="section">
            <div class="section-title">
                <span class="emoji">🤖</span>
                <span>AI视频行业新动态</span>
            </div>
            <div class="cards" id="aiNewsCards">
                {generate_ai_cards(data['ai_news'])}
            </div>
        </section>

        <section class="section">
            <div class="section-title">
                <span class="emoji">🎭</span>
                <span>舞台设备资讯</span>
            </div>
            <div class="cards" id="stageEquipmentCards">
                {generate_stage_cards(data['stage_equipment'])}
            </div>
        </section>
    </main>

    <footer>
        <div class="update-time">数据自动更新于：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        <div>数据来源：FB & INS Reels · 行业公开资讯 · 仅供学习参考</div>
    </footer>
</body>
</html>'''
    
    # 保存 HTML
    with open('/workspace/每日简报-完整版/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ HTML 生成成功！")

def generate_social_cards(items):
    """生成社媒卡片"""
    cards_html = ''
    for item in items:
        cards_html += f'''
                <article class="card">
                    <h3 class="card-title">
                        <span class="highlight">[{item['platform']}]</span> {item['title']}
                    </h3>
                    <div class="card-meta">
                        <span class="platform">{item['platform']}</span>
                        <span>{item['time']}</span>
                    </div>
                    <img src="{item['image']}" alt="{item['title']}" class="card-image" loading="lazy">
                    <p class="card-content">{item['summary']}</p>
                    <a href="{item['link']}" class="card-link" target="_blank" rel="noopener noreferrer">查看详情</a>
                </article>
        '''
    return cards_html

def generate_ai_cards(items):
    """生成AI新闻卡片"""
    cards_html = ''
    for item in items:
        features_html = ''
        if 'features' in item:
            features_html = ''.join([f'<li>{f}</li>' for f in item['features']])
            features_html = f'<ul class="feature-list">{features_html}</ul>'
        
        cards_html += f'''
                <article class="card">
                    <span class="info-tag">{item['tag']}</span>
                    <h3 class="card-title">{item['title']}</h3>
                    <div class="card-meta">
                        <span>📰 {item['source']}</span>
                        <span>🕐 {item['time']}</span>
                    </div>
                    <img src="{item['image']}" alt="{item['title']}" class="card-image" loading="lazy">
                    <p class="card-content">{item['summary']}</p>
                    {features_html}
                    <a href="{item['link']}" class="card-link" target="_blank" rel="noopener noreferrer">了解更多</a>
                </article>
        '''
    return cards_html

def generate_stage_cards(items):
    """生成舞台设备卡片"""
    cards_html = ''
    for item in items:
        highlights_html = ''
        if 'highlights' in item:
            highlights_html = ''.join([f'<li>{h}</li>' for h in item['highlights']])
            highlights_html = f'<ul class="feature-list">{highlights_html}</ul>'
        
        cards_html += f'''
                <article class="card">
                    <h3 class="card-title">
                        <span class="highlight">[{item['vendor']}]</span> {item['title']}
                    </h3>
                    <div class="card-meta">
                        <span class="platform">{item['vendor']}</span>
                        <span>{item['time']}</span>
                    </div>
                    <img src="{item['image']}" alt="{item['title']}" class="card-image" loading="lazy">
                    <p class="card-content">{item['summary']}</p>
                    {highlights_html}
                    <a href="{item['link']}" class="card-link" target="_blank" rel="noopener noreferrer">查看产品</a>
                </article>
        '''
    return cards_html

if __name__ == '__main__':
    generate_html()
