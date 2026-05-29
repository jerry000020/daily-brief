# 海外创意·AI视频·舞台设备 每日简报

## 📋 项目简介

这是一个完全自动化的每日简报系统，每天 08:00 自动生成并部署到 GitHub Pages。

### 🎯 三大板块

- **🔥 FB & INS 创意视频**：Facebook & Instagram 近24小时热门内容（3条）
- **🤖 AI视频行业动态**：Runway、Pika、Kling、Luma 最新资讯（4条）
- **🎭 舞台设备最新资讯**：专业灯光、控台设备、新品资讯（3条）

## 🚀 快速开始

### 方式一：手动生成（推荐）

```bash
python main.py
```

### 方式二：一键部署

```bash
# Windows PowerShell
.\deploy.ps1
```

## 📁 项目结构

```
.
├── main.py              # 主程序（生成数据 + HTML）
├── crawler.py           # Playwright 爬虫框架
├── deploy.ps1           # GitHub 一键部署脚本
├── index.html           # 生成的网页文件
└── README.md            # 说明文档
```

## 🎨 设计规范

- **主色**：`#165DFF`
- **强调色**：`#FF7D00`
- **响应式**：手机/电脑完美适配
- **卡片设计**：圆角 + 阴影 + 悬停效果

## ⚙️ 配置

在 `main.py` 顶部可以修改配置：

```python
CONFIG = {
    "github_repo": "https://github.com/jerry000020/daily-brief",
    "web_url": "https://jerry000020.github.io/daily-brief/",
    "primary_color": "#165DFF",
    "accent_color": "#FF7D00"
}
```

## 📊 数据来源

### 🎬 视频数据
- Facebook: `https://www.facebook.com/watch/?v=xxx`
- Instagram: `https://www.instagram.com/reel/xxx/`

### 🤖 AI 动态
- Runway: https://runwayml.com
- Pika: https://pika.art
- Kling: https://klingai.com
- Luma: https://lumalabs.ai

## 📝 注意事项

### 关于真实爬虫

由于 Facebook 和 Instagram 有严格的反爬机制，真实爬取需要：
1. 配置代理 IP
2. 使用真实账户登录
3. 遵守平台服务条款

本项目使用模拟数据生成器，可以直接使用。如需接入真实爬虫，请参考 `crawler.py` 进行扩展。

### 定时任务

配置 GitHub Actions 或 Trae 定时任务：
- 执行时间：每天 08:00
- 执行命令：`python main.py && git add . && git commit -m "每日更新" && git push`

## 📞 访问

- **网页地址**：https://jerry000020.github.io/daily-brief/
- **仓库地址**：https://github.com/jerry000020/daily-brief

## 📄 License

MIT License
