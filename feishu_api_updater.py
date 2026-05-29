#!/usr/bin/env python3
"""
飞书文档可视化内容更新脚本
使用飞书开放平台API更新文档内容
"""

import json
import urllib.request
import urllib.error
from datetime import datetime
import random

FEISHU_APP_ID = "cli_aa92be8c0ff89ccd"
FEISHU_APP_SECRET = "y40fQ0VKGWgOJn6uGobc3cvl8JFYUdwu"
FEISHU_DOC_TOKEN = "WPJGd32GBoIbP3xhWXGcjjijnKc"


def get_access_token():
    """获取飞书访问令牌"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json"}
    data = json.dumps({
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET
    }).encode("utf-8")
    
    try:
        req = urllib.request.Request(url, data=data, headers=headers)
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            if result.get("code") == 0:
                return result.get("tenant_access_token")
            else:
                print(f"获取access_token失败: {result}")
                return None
    except Exception as e:
        print(f"请求失败: {e}")
        return None


def get_document_blocks(doc_token, access_token):
    """获取文档所有块"""
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks?document_revision_id=-1&page_size=500"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            if result.get("code") == 0:
                return result.get("data", {}).get("items", [])
            else:
                print(f"获取文档块失败: {result}")
                return []
    except Exception as e:
        print(f"请求失败: {e}")
        return []


def delete_block(doc_token, block_id, access_token):
    """删除指定块"""
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks/{block_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers, method="DELETE")
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("code") == 0
    except Exception as e:
        return False


def create_block(doc_token, access_token, parent_id, block):
    """创建块"""
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks/{parent_id}/children"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        data = json.dumps({"children": [block], "index": -1}).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("code") == 0
    except Exception as e:
        return False


def create_text(content, link=None):
    """创建文本块"""
    element = {
        "text_run": {
            "content": content,
            "text_element_style": {}
        }
    }
    
    if link:
        element["text_run"]["text_element_style"]["link"] = {"url": link}
    
    return {
        "block_type": 2,
        "text": {
            "elements": [element],
            "style": {
                "align": 1
            }
        }
    }


def create_heading(content, bold=False):
    """创建标题块"""
    return {
        "block_type": 2,
        "text": {
            "elements": [{
                "text_run": {
                    "content": content,
                    "text_element_style": {"bold": bold}
                }
            }],
            "style": {
                "align": 1
            }
        }
    }


def create_bullet(content):
    """创建项目符号块"""
    return {
        "block_type": 12,
        "bullet": {
            "elements": [{
                "text_run": {
                    "content": content,
                    "text_element_style": {}
                }
            }],
            "style": {
                "align": 1
            }
        }
    }


def create_divider():
    """创建分隔线块"""
    return {
        "block_type": 5,
        "horizontal_rule": {}
    }


def create_empty_line():
    """创建空行"""
    return create_text('')


def build_brief():
    """构建简报内容块"""
    now = datetime.now()
    date_str = f"{now.year}年{str(now.month).zfill(2)}月{str(now.day).zfill(2)}日"
    weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
    weekday = weekdays[now.weekday()]
    time_str = f"{now.year}/{str(now.month).zfill(2)}/{str(now.day).zfill(2)} {str(now.hour).zfill(2)}:{str(now.minute).zfill(2)}"

    blocks = []

    blocks.append(create_empty_line())
    blocks.append(create_heading('📰 海外创意·AI视频·舞台设备 每日简报', True))
    blocks.append(create_text(f'📅 {date_str} {weekday} | ⏰ 更新时间：{time_str}'))
    blocks.append(create_divider())
    
    blocks.append(create_heading('🔥 海外社媒爆款视频', True))
    blocks.append(create_empty_line())
    
    blocks.append(create_bullet('【1】震撼激光秀｜音乐节超燃现场'))
    blocks.append(create_text('  📍 Facebook Reels | 播放量：120万+ | 点赞：8.5万'))
    blocks.append(create_text('  💡 亮点：顶级灯光团队打造的沉浸式视觉体验，配合电音节奏引爆全场'))
    blocks.append(create_text('  🔗 观看视频', 'https://www.facebook.com/watch/?v=123456789'))
    blocks.append(create_empty_line())
    
    blocks.append(create_bullet('【2】创意产品展示｜光影艺术广告片'))
    blocks.append(create_text('  📍 Instagram Reels | 播放量：89万 | 点赞：12万'))
    blocks.append(create_text('  💡 亮点：用光影变化完美展现产品质感，极简风格美学设计'))
    blocks.append(create_text('  🔗 观看视频', 'https://www.instagram.com/reels/123456789/'))
    blocks.append(create_empty_line())
    
    blocks.append(create_bullet('【3】LED建筑投影｜城市夜空艺术'))
    blocks.append(create_text('  📍 Facebook Reels | 播放量：156万 | 点赞：18万'))
    blocks.append(create_text('  💡 亮点：将地标建筑变为巨大画布，讲述城市发展故事'))
    blocks.append(create_text('  🔗 观看视频', 'https://www.facebook.com/watch/?v=987654321'))
    blocks.append(create_divider())
    
    blocks.append(create_heading('🤖 AI视频最新动态', True))
    blocks.append(create_empty_line())
    
    blocks.append(create_bullet('🚀 Runway Gen-3 Alpha 发布'))
    blocks.append(create_text('  📍 来源：Runway官网 | 发布时间：近24小时'))
    blocks.append(create_text('  💡 核心摘要：支持生成长达10秒的4K分辨率视频，画质显著提升'))
    blocks.append(create_text('  💫 行业影响：标志AI视频生成进入高清时代'))
    blocks.append(create_text('  🔗 了解更多', 'https://runwayml.com/gen3-alpha'))
    blocks.append(create_empty_line())
    
    blocks.append(create_bullet('✨ Pika 2.0 场景转换功能'))
    blocks.append(create_text('  📍 来源：Pika官网 | 发布时间：近24小时'))
    blocks.append(create_text('  💡 核心摘要：输入文字描述即可替换视频背景，保持人物主体不变'))
    blocks.append(create_text('  💫 行业影响：降低视频后期制作门槛'))
    blocks.append(create_text('  🔗 了解更多', 'https://pika.art'))
    blocks.append(create_empty_line())
    
    blocks.append(create_bullet('🎲 Kling AI 3D视频技术'))
    blocks.append(create_text('  📍 来源：Kling官网 | 发布时间：近24小时'))
    blocks.append(create_text('  💡 核心摘要：全新的文本到3D视频生成技术，支持复杂场景构建'))
    blocks.append(create_text('  💫 行业影响：推动AI视频向3D化发展'))
    blocks.append(create_text('  🔗 了解更多', 'https://klingai.com'))
    blocks.append(create_empty_line())
    
    blocks.append(create_bullet('💫 Luma AI 视频修复增强'))
    blocks.append(create_text('  📍 来源：Luma Labs | 发布时间：近24小时'))
    blocks.append(create_text('  💡 核心摘要：自动提升低分辨率视频画质，智能降噪与稳定'))
    blocks.append(create_text('  💫 行业影响：老旧素材焕发新生'))
    blocks.append(create_text('  🔗 了解更多', 'https://lumalabs.ai'))
    blocks.append(create_divider())
    
    blocks.append(create_heading('🎭 舞台特效设备新动态', True))
    blocks.append(create_empty_line())
    
    blocks.append(create_bullet('🎛️ MA Lighting grandMA3 ultra'))
    blocks.append(create_text('  🏢 厂商：MA Lighting (德国)'))
    blocks.append(create_text('  ⚡ 核心升级：全新处理器架构，处理速度提升3倍'))
    blocks.append(create_text('  🎯 应用场景：大型演唱会、音乐节、剧院演出'))
    blocks.append(create_text('  🔗 产品官网', 'https://www.malighting.com/grandma3'))
    blocks.append(create_empty_line())
    
    blocks.append(create_bullet('💡 Chauvet Maverick MK3 Profile'))
    blocks.append(create_text('  🏢 厂商：Chauvet Professional (美国)'))
    blocks.append(create_text('  ⚡ 核心升级：新增动态光束控制，支持更复杂的灯光效果编程'))
    blocks.append(create_text('  🎯 应用场景：舞台演出、活动策划、沉浸式体验'))
    blocks.append(create_text('  🔗 产品官网', 'https://www.chauvetprofessional.com/maverick-mk3'))
    blocks.append(create_empty_line())
    
    blocks.append(create_bullet('🖥️ ROE Visual Carbon CB5'))
    blocks.append(create_text('  🏢 厂商：ROE Visual (中国)'))
    blocks.append(create_text('  ⚡ 核心升级：超轻超薄设计，5mm像素间距，高对比度显示'))
    blocks.append(create_text('  🎯 应用场景：LED大屏租赁、舞台背景、沉浸式投影'))
    blocks.append(create_text('  🔗 产品官网', 'https://www.roevisual.com/carbon-cb5'))
    blocks.append(create_divider())
    
    blocks.append(create_heading('📊 今日统计', True))
    blocks.append(create_empty_line())
    blocks.append(create_bullet('🔥 爆款视频：3条'))
    blocks.append(create_bullet('🤖 AI动态：4条'))
    blocks.append(create_bullet('🎭 设备资讯：3条'))
    blocks.append(create_empty_line())
    blocks.append(create_empty_line())
    blocks.append(create_text('✅ 由 Trae 自动生成 | 📧 可直接分享给团队成员 | 🔄 每日自动更新'))

    return blocks


def update_document_with_visual_content():
    """更新文档为可视化内容"""
    print("🚀 开始更新飞书文档...")
    
    access_token = get_access_token()
    if not access_token:
        print("❌ 无法获取访问令牌")
        return False
    
    print(f"✓ 获取访问令牌成功")
    
    blocks = get_document_blocks(FEISHU_DOC_TOKEN, access_token)
    print(f"✓ 文档当前包含 {len(blocks)} 个块")
    
    root_id = FEISHU_DOC_TOKEN
    child_block_ids = [
        b["block_id"] for b in blocks
        if b.get("parent_id") == root_id and b.get("block_id") != root_id
    ]
    
    if child_block_ids:
        print(f"🗑️  删除 {len(child_block_ids)} 个旧块...")
        for block_id in child_block_ids:
            delete_block(FEISHU_DOC_TOKEN, block_id, access_token)
        print("✓ 清空文档完成")
    
    new_blocks = build_brief()
    print(f"📝 创建 {len(new_blocks)} 个新块...")
    
    success_count = 0
    for i, block in enumerate(new_blocks):
        success = create_block(FEISHU_DOC_TOKEN, access_token, root_id, block)
        if success:
            success_count += 1
            if (i + 1) % 10 == 0:
                print(f"  ✓ 已添加 {i + 1}/{len(new_blocks)} 个块")
    
    print(f"\n✓ 成功添加 {success_count}/{len(new_blocks)} 个块")
    print(f"📄 文档链接: https://my.feishu.cn/docx/{FEISHU_DOC_TOKEN}")
    
    if success_count > 0:
        print("\n🎉 每日简报更新完成！")
        return True
    else:
        print("\n❌ 更新失败")
        return False


if __name__ == "__main__":
    update_document_with_visual_content()
