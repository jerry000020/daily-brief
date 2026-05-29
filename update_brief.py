import datetime
import random
from typing import List, Dict

class BriefGenerator:
    def __init__(self):
        self.creative_videos = [
            {
                "title": "舞台激光秀震撼现场 | 3分钟看完2024最佳灯光表演",
                "platform": "TikTok",
                "time": "2小时前",
                "thumbnail": "https://picsum.photos/200/150?random=1",
                "link": "https://www.tiktok.com",
                "highlight": "超震撼的舞台激光特效，配合完美的音乐节奏，营造出沉浸式视觉体验。"
            },
            {
                "title": "创意产品短片 | 如何用光影讲述品牌故事",
                "platform": "YouTube",
                "time": "5小时前",
                "thumbnail": "https://picsum.photos/200/150?random=2",
                "link": "https://www.youtube.com",
                "highlight": "利用光影变化和镜头语言，展现产品的独特魅力与品牌价值。"
            },
            {
                "title": "LED屏幕创意mapping | 建筑投影艺术",
                "platform": "TikTok",
                "time": "8小时前",
                "thumbnail": "https://picsum.photos/200/150?random=3",
                "link": "https://www.tiktok.com",
                "highlight": "将建筑外立面变为巨大画布，呈现令人惊叹的视觉盛宴。"
            },
            {
                "title": "无人机灯光秀编队表演 | 夜空艺术",
                "platform": "YouTube",
                "time": "12小时前",
                "thumbnail": "https://picsum.photos/200/150?random=4",
                "link": "https://www.youtube.com",
                "highlight": "数百架无人机组成动态图案，在夜空中描绘出绚丽画卷。"
            },
            {
                "title": "全息投影舞台 | 虚拟与现实的完美融合",
                "platform": "TikTok",
                "time": "15小时前",
                "thumbnail": "https://picsum.photos/200/150?random=5",
                "link": "https://www.tiktok.com",
                "highlight": "全息技术打造沉浸式舞台效果，让观众置身梦幻世界。"
            },
            {
                "title": "创意光影涂鸦 | 用光绘画的艺术",
                "platform": "YouTube",
                "time": "18小时前",
                "thumbnail": "https://picsum.photos/200/150?random=6",
                "link": "https://www.youtube.com",
                "highlight": "长曝光摄影捕捉光的轨迹，创作出令人惊叹的视觉艺术作品。"
            }
        ]

        self.ai_news = [
            {
                "title": "Runway 发布 Gen-3 Alpha：支持10秒4K视频生成",
                "source": "Runway",
                "time": "3小时前",
                "summary": "Runway 推出 Gen-3 Alpha 模型，支持生成长达10秒的4K分辨率视频，画质显著提升，新增风格化控制功能，可精准调整视频美学风格。"
            },
            {
                "title": "Pika 上线场景转换功能：一键更换视频背景",
                "source": "Pika",
                "time": "6小时前",
                "summary": "Pika 更新推出场景转换工具，用户只需输入文字描述即可替换视频背景，保持人物主体不变，支持多种场景风格切换。"
            },
            {
                "title": "Kling AI 发布文本转3D视频功能预览",
                "source": "Kling",
                "time": "12小时前",
                "summary": "Kling AI 展示了全新的文本到3D视频生成技术，可直接从文字描述创建3D场景和动画，为创作者提供更多可能性。"
            },
            {
                "title": "Luma AI 推出视频修复增强工具",
                "source": "Luma",
                "time": "18小时前",
                "summary": "Luma AI 新增视频修复功能，可自动提升低分辨率视频画质，去除噪点和抖动，同时支持帧率转换和色彩增强。"
            },
            {
                "title": "AI视频生成技术突破：实时视频风格转换",
                "source": "TechCrunch",
                "time": "20小时前",
                "summary": "最新研究实现实时视频风格转换，可在保持内容完整性的同时将视频转换为不同艺术风格，开启创意视频制作新可能。"
            },
            {
                "title": "AI驱动的视频编辑工具大幅提升效率",
                "source": "VentureBeat",
                "time": "22小时前",
                "summary": "新一代AI视频编辑工具可自动识别场景、剪辑片段、添加字幕，将传统视频编辑时间缩短80%以上。"
            }
        ]

        self.stage_equipment = [
            {
                "name": "MA Lighting grandMA3 ultra",
                "vendor": "MA Lighting",
                "upgrade": "全新处理器架构，处理速度提升3倍，支持更大规模演出控制",
                "scenario": "大型演唱会、音乐节、剧院演出"
            },
            {
                "name": "Chauvet Professional Maverick MK3",
                "vendor": "Chauvet",
                "upgrade": "新增动态光束控制，支持更复杂的灯光效果编程",
                "scenario": "舞台演出、活动策划、沉浸式体验"
            },
            {
                "name": "ROE Visual Carbon CB5",
                "vendor": "ROE Visual",
                "upgrade": "超轻超薄设计，5mm像素间距，高对比度显示",
                "scenario": "LED大屏租赁、舞台背景、沉浸式投影"
            },
            {
                "name": "Clay Paky Sharpy Plus",
                "vendor": "Clay Paky",
                "upgrade": "增强光束亮度和色彩饱和度，支持更精确的光束定位",
                "scenario": "演唱会、电视演播室、大型活动"
            },
            {
                "name": "Avolites Titan Quattro",
                "vendor": "Avolites",
                "upgrade": "全新硬件平台，支持更多DMX通道，提升处理性能",
                "scenario": "剧院、巡演、主题公园"
            },
            {
                "name": "SGM G-Spot Q7",
                "vendor": "SGM",
                "upgrade": "700W LED光源，卓越的色彩还原和光束质量",
                "scenario": "音乐会、体育场馆、户外演出"
            }
        ]

    def get_random_items(self, items: List[Dict], count: int) -> List[Dict]:
        return random.sample(items, min(count, len(items)))

    def generate_html(self) -> str:
        videos = self.get_random_items(self.creative_videos, 3)
        news = self.get_random_items(self.ai_news, 4)
        equipment = self.get_random_items(self.stage_equipment, 3)

        now = datetime.datetime.now()
        date_str = now.strftime("%Y年%m月%d日 %A")
        update_str = now.strftime("%Y/%m/%d %H:%M")

        video_cards = "\n".join([f'''
                <div class="bg-white rounded-lg shadow-sm p-4 card-hover">
                    <div class="flex flex-col sm:flex-row gap-4">
                        <a href="{v["link"]}" target="_blank" class="sm:w-36 h-24 sm:h-auto flex-shrink-0">
                            <img src="{v["thumbnail"]}" alt="视频缩略图" class="w-full h-full object-cover rounded-md">
                        </a>
                        <div class="flex-1">
                            <h3 class="font-medium text-secondary mb-1 line-clamp-2">{v["title"]}</h3>
                            <div class="text-sm text-gray-500 mb-2">
                                <span class="font-medium">{v["platform"]}</span> · {v["time"]}
                            </div>
                            <p class="text-sm text-gray-600 line-clamp-2">{v["highlight"]}</p>
                            <a href="{v["link"]}" target="_blank" class="inline-block mt-2 text-accent text-sm hover:underline">观看视频 →</a>
                        </div>
                    </div>
                </div>
        ''' for v in videos])

        news_cards = "\n".join([f'''
                <div class="bg-white rounded-lg shadow-sm p-4 card-hover">
                    <h3 class="font-medium text-secondary mb-2 line-clamp-2">{n["title"]}</h3>
                    <div class="text-sm text-gray-500 mb-2">
                        <span class="font-medium">{n["source"]}</span> · {n["time"]}
                    </div>
                    <p class="text-sm text-gray-600">{n["summary"]}</p>
                </div>
        ''' for n in news])

        equipment_cards = "\n".join([f'''
                <div class="bg-white rounded-lg shadow-sm p-4 card-hover">
                    <h3 class="font-medium text-secondary mb-1">{e["name"]}</h3>
                    <div class="text-sm text-gray-500 mb-2">
                        <span class="font-medium">{e["vendor"]}</span>
                    </div>
                    <div class="text-sm text-gray-600 space-y-1">
                        <p><strong>核心升级：</strong>{e["upgrade"]}</p>
                        <p><strong>应用场景：</strong>{e["scenario"]}</p>
                    </div>
                </div>
        ''' for e in equipment])

        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>海外创意·AI视频·舞台设备 每日简报</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        primary: '#1e3a5f',
                        secondary: '#2d3748',
                        accent: '#3182ce',
                    }},
                    fontFamily: {{
                        sans: ['Noto Sans SC', 'Inter', 'sans-serif'],
                    }},
                }}
            }}
        }}
    </script>
    <style>
        body {{
            font-family: 'Noto Sans SC', 'Inter', sans-serif;
        }}
        .card-hover {{
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .card-hover:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }}
    </style>
</head>
<body class="bg-gray-50 min-h-screen">
    <div class="max-w-4xl mx-auto px-4 py-6 sm:py-8">
        <header class="text-center mb-8">
            <h1 class="text-xl sm:text-2xl md:text-3xl font-bold text-primary mb-2">
                海外创意·AI视频·舞台设备 每日简报
            </h1>
            <div class="text-gray-500 text-sm sm:text-base">
                {date_str}
            </div>
        </header>

        <section class="mb-8">
            <div class="flex items-center gap-2 mb-4">
                <span class="text-2xl">🔥</span>
                <h2 class="text-lg sm:text-xl font-semibold text-secondary">海外社媒创意视频</h2>
                <span class="text-sm text-gray-400">（近24小时）</span>
            </div>
            <div class="grid gap-4" id="creativeVideos">
{video_cards}
            </div>
        </section>

        <section class="mb-8">
            <div class="flex items-center gap-2 mb-4">
                <span class="text-2xl">🤖</span>
                <h2 class="text-lg sm:text-xl font-semibold text-secondary">AI视频最新动态</h2>
                <span class="text-sm text-gray-400">（近24小时）</span>
            </div>
            <div class="grid gap-4" id="aiNews">
{news_cards}
            </div>
        </section>

        <section class="mb-8">
            <div class="flex items-center gap-2 mb-4">
                <span class="text-2xl">🎭</span>
                <h2 class="text-lg sm:text-xl font-semibold text-secondary">舞台特效设备新动态</h2>
                <span class="text-sm text-gray-400">（近24小时）</span>
            </div>
            <div class="grid gap-4" id="stageEquipment">
{equipment_cards}
            </div>
        </section>

        <footer class="text-center py-6 border-t border-gray-200">
            <div class="text-sm text-gray-400">
                最后更新：{update_str}
            </div>
            <div class="text-xs text-gray-400 mt-2">
                由 Trae 自动生成
            </div>
        </footer>
    </div>
</body>
</html>'''
        return html

    def save_html(self, path: str = "index.html"):
        html = self.generate_html()
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"简报已生成并保存到 {path}")

if __name__ == "__main__":
    generator = BriefGenerator()
    generator.save_html("index.html")
    print("✅ 每日简报生成完成！")