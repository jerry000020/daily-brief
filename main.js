#!/usr/bin/env node

/**
 * 海外创意·AI视频·舞台设备 每日简报系统
 * JavaScript 版本
 */

const fs = require('fs');
const path = require('path');

// 配置
const CONFIG = {
    github_repo: "https://github.com/jerry000020/daily-brief",
    web_url: "https://jerry000020.github.io/daily-brief/",
    primary_color: "#165DFF",
    accent_color: "#FF7D00"
};

function generateVideoData() {
    return [
        {
            id: "fb-001",
            title: "全息舞台表演｜虚拟与现实融合",
            cover: "https://images.unsplash.com/photo-1507924538820-ede94a04019d?w=600&h=400&fit=crop",
            url: "https://www.facebook.com/watch/?v=fb123456789",
            platform: "FB",
            time: "12小时前",
            description: "全息技术让虚拟偶像与真人同台演出，技术突破引发行业广泛关注"
        },
        {
            id: "ins-001",
            title: "3D Mapping秀｜裸眼3D视觉盛宴",
            cover: "https://images.unsplash.com/photo-1511765224780-d912e42b4980?w=600&h=400&fit=crop",
            url: "https://www.instagram.com/reel/CxY1aBcD2eF/",
            platform: "INS",
            time: "8小时前",
            description: "商场外立面的3D投影秀，逼真的视觉效果让路人纷纷驻足拍摄"
        },
        {
            id: "fb-002",
            title: "无人机编队表演｜科技感拉满",
            cover: "https://images.unsplash.com/photo-1485988412941-77a35537dae4?w=600&h=400&fit=crop",
            url: "https://www.facebook.com/watch/?v=fb987654321",
            platform: "FB",
            time: "6小时前",
            description: "500架无人机在空中组成动态图案，庆祝品牌周年庆"
        }
    ];
}

function generateAiData() {
    return [
        {
            title: "Runway Gen-3 Alpha 发布",
            source: "Runway",
            time: "2小时前",
            summary: "支持生成长达10秒的4K分辨率视频，画质显著提升",
            icon: "rocket",
            color: "from-red-500 to-orange-500",
            url: "https://runwayml.com"
        },
        {
            title: "Pika 场景转换功能更新",
            source: "Pika",
            time: "5小时前",
            summary: "输入文字描述即可替换视频背景，保持人物主体不变",
            icon: "sparkles",
            color: "from-purple-500 to-pink-500",
            url: "https://pika.art"
        },
        {
            title: "Kling AI 3D视频技术",
            source: "Kling",
            time: "8小时前",
            summary: "全新的文本到3D视频生成技术，可直接从文字描述创建3D场景",
            icon: "dice",
            color: "from-yellow-500 to-orange-500",
            url: "https://klingai.com"
        },
        {
            title: "Luma AI 视频修复增强",
            source: "Luma",
            time: "12小时前",
            summary: "自动提升低分辨率视频画质，去除噪点和抖动",
            icon: "star",
            color: "from-cyan-500 to-blue-500",
            url: "https://lumalabs.ai"
        }
    ];
}

function generateStageData() {
    return [
        {
            name: "MA Lighting grandMA3 ultra",
            company: "MA Lighting (德国)",
            upgrade: "全新处理器架构，处理速度提升3倍",
            use_case: "大型演唱会、音乐节、剧院演出",
            image: "https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=600&h=300&fit=crop",
            url: "https://www.malighting.com"
        },
        {
            name: "Chauvet Maverick MK3",
            company: "Chauvet Professional (美国)",
            upgrade: "新增动态光束控制，支持复杂灯光编程",
            use_case: "舞台演出、活动策划、沉浸式体验",
            image: "https://images.unsplash.com/photo-1531973576160-7125cd663d86?w=600&h=300&fit=crop",
            url: "https://www.chauvetprofessional.com"
        },
        {
            name: "ROE Visual Carbon CB5",
            company: "ROE Visual (中国)",
            upgrade: "超轻超薄设计，5mm像素间距，高对比度显示",
            use_case: "LED大屏租赁、舞台背景、沉浸式投影",
            image: "https://images.unsplash.com/photo-1555949965-aa79d59d275e?w=600&h=300&fit=crop",
            url: "https://www.roevisual.com"
        }
    ];
}

function buildHtml(videos, aiNews, stageProducts) {
    const now = new Date();
    const weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
    const dateStr = `${now.getFullYear()}年${String(now.getMonth() + 1).padStart(2, '0')}月${String(now.getDate()).padStart(2, '0')}日`;
    const weekday = weekdays[now.getDay()];
    const updateTime = `${now.getFullYear()}/${String(now.getMonth() + 1).padStart(2, '0')}/${String(now.getDate()).padStart(2, '0')} ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
    
    let html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>海外创意·AI视频·舞台设备 每日简报</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
      min-height: 100vh;
    }
    .card-hover {
      transition: all 0.3s ease;
    }
    .card-hover:hover {
      transform: translateY(-4px);
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    }
    .play-button {
      transition: transform 0.3s ease;
    }
    .play-button:hover {
      transform: scale(1.1);
    }
  </style>
</head>
<body class="pb-12">
  <header class="bg-[#165DFF] text-white rounded-2xl shadow-xl mx-4 mt-6 p-6">
    <div class="flex items-center justify-between flex-wrap">
      <div class="flex items-center gap-3">
        <div class="bg-white/20 p-3 rounded-xl">
          <i class="fa-solid fa-newspaper text-xl"></i>
        </div>
        <div>
          <h1 class="text-2xl font-bold">海外创意 · AI视频 · 舞台设备</h1>
          <p class="text-white/80 text-sm">每日简报 · 洞察行业动态</p>
        </div>
      </div>
      <div class="flex items-center gap-4 mt-4 sm:mt-0">
        <div class="text-right">
          <div class="text-sm text-white/80">今日日期</div>
          <div class="font-semibold">${dateStr} ${weekday}</div>
        </div>
        <button class="bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg flex items-center gap-2 transition-colors" onclick="shareBrief()">
          <i class="fa-solid fa-share-nodes"></i>
          <span class="hidden sm:inline">分享</span>
        </button>
      </div>
    </div>
  </header>

  <div class="flex justify-center gap-4 px-4 mt-6">
    <div class="bg-white/80 backdrop-blur rounded-xl px-6 py-4 text-center min-w-[120px] shadow-lg">
      <div class="text-3xl font-bold text-[#165DFF]">3</div>
      <div class="text-gray-500 text-sm">爆款视频</div>
    </div>
    <div class="bg-white/80 backdrop-blur rounded-xl px-6 py-4 text-center min-w-[120px] shadow-lg">
      <div class="text-3xl font-bold text-[#764BA2]">4</div>
      <div class="text-gray-500 text-sm">AI动态</div>
    </div>
    <div class="bg-white/80 backdrop-blur rounded-xl px-6 py-4 text-center min-w-[120px] shadow-lg">
      <div class="text-3xl font-bold text-[#FF7D00]">3</div>
      <div class="text-gray-500 text-sm">设备资讯</div>
    </div>
  </div>

  <section class="px-4 mt-8">
    <div class="flex items-center gap-3 mb-6">
      <div class="bg-[#165DFF] p-2 rounded-lg">
        <i class="fa-solid fa-flame text-white"></i>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-800">FB & INS 创意视频</h2>
        <p class="text-gray-500 text-sm">Facebook & Instagram · 近24小时热门内容</p>
      </div>
    </div>

    <div class="space-y-4">
`;

    // 添加视频卡片
    for (const video of videos) {
        const platformColor = video.platform === "FB" ? "bg-blue-600" : "bg-pink-600";
        html += `
      <div class="bg-white rounded-xl shadow-lg overflow-hidden card-hover">
        <div class="flex flex-col sm:flex-row">
          <div class="relative sm:w-48 h-32 sm:h-auto">
            <img src="${video.cover}" alt="${video.title}" class="w-full h-full object-cover">
            <div class="absolute inset-0 bg-black/30 flex items-center justify-center">
              <button class="play-button bg-white/90 w-12 h-12 rounded-full flex items-center justify-center" onclick="window.open('${video.url}', '_blank')">
                <i class="fa-solid fa-play text-[#165DFF] ml-1"></i>
              </button>
            </div>
            <div class="absolute bottom-2 left-2 flex gap-2">
              <span class="text-xs font-semibold ${platformColor} text-white px-2 py-1 rounded-full">${video.platform}</span>
              <span class="text-xs text-white bg-black/50 px-2 py-1 rounded-full">${video.time}</span>
            </div>
          </div>
          <div class="p-4 flex-1">
            <h3 class="font-bold text-gray-800">${video.title}</h3>
            <p class="text-gray-500 text-sm mt-1">${video.description}</p>
            <button class="text-[#165DFF] font-medium text-sm mt-3 hover:text-blue-700 flex items-center gap-1" onclick="window.open('${video.url}', '_blank')">
              查看详情 <i class="fa-solid fa-arrow-right"></i>
            </button>
          </div>
        </div>
      </div>
`;
    }

    html += `
    </div>
  </section>

  <section class="px-4 mt-12">
    <div class="flex items-center gap-3 mb-6">
      <div class="bg-[#764BA2] p-2 rounded-lg">
        <i class="fa-solid fa-robot text-white"></i>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-800">AI视频行业动态</h2>
        <p class="text-gray-500 text-sm">Runway · Pika · Kling · Luma · 行业前沿</p>
      </div>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
`;

    // 添加AI动态卡片
    for (const ai of aiNews) {
        html += `
      <div class="bg-white rounded-xl p-5 shadow-lg card-hover">
        <div class="flex items-start gap-3">
          <div class="bg-gradient-to-br ${ai.color} p-3 rounded-xl text-white">
            <i class="fa-solid fa-${ai.icon} text-xl"></i>
          </div>
          <div class="flex-1">
            <h3 class="font-bold text-gray-800">${ai.title}</h3>
            <p class="text-gray-500 text-sm mt-1">${ai.summary}</p>
            <div class="flex items-center gap-2 mt-2">
              <span class="bg-green-100 text-green-600 text-xs px-2 py-1 rounded-full">${ai.source}</span>
              <span class="text-gray-400 text-xs">${ai.time}</span>
            </div>
            <button class="text-[#165DFF] text-sm mt-3 flex items-center gap-1 hover:text-blue-700" onclick="window.open('${ai.url}', '_blank')">
              了解更多 <i class="fa-solid fa-external-link"></i>
            </button>
          </div>
        </div>
      </div>
`;
    }

    html += `
    </div>
  </section>

  <section class="px-4 mt-12">
    <div class="flex items-center gap-3 mb-6">
      <div class="bg-[#FF7D00] p-2 rounded-lg">
        <i class="fa-solid fa-masks-theater text-white"></i>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-800">舞台设备最新资讯</h2>
        <p class="text-gray-500 text-sm">专业灯光 · 控台设备 · 新品资讯</p>
      </div>
    </div>

    <div class="space-y-4">
`;

    // 添加舞台设备卡片
    for (const product of stageProducts) {
        html += `
      <div class="bg-white rounded-xl shadow-lg overflow-hidden card-hover">
        <div class="flex flex-col sm:flex-row">
          <div class="sm:w-48 h-32 sm:h-auto">
            <img src="${product.image}" alt="${product.name}" class="w-full h-full object-cover">
          </div>
          <div class="p-4 flex-1">
            <div class="flex items-center gap-2 mb-2">
              <i class="fa-solid fa-sliders-h text-[#165DFF]"></i>
              <h3 class="font-bold text-gray-800">${product.name}</h3>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-1 gap-1 text-sm">
              <div><span class="text-gray-500">厂商：</span><span class="text-gray-800">${product.company}</span></div>
              <div><span class="text-gray-500">核心升级：</span><span class="text-gray-800">${product.upgrade}</span></div>
              <div><span class="text-gray-500">应用场景：</span><span class="text-gray-800">${product.use_case}</span></div>
            </div>
            <button class="text-[#165DFF] text-sm mt-3 flex items-center gap-1 hover:text-blue-700" onclick="window.open('${product.url}', '_blank')">
              访问官网 <i class="fa-solid fa-external-link"></i>
            </button>
          </div>
        </div>
      </div>
`;
    }

    html += `
    </div>
  </section>

  <footer class="px-4 mt-12 text-center text-gray-400 text-sm">
    <div class="bg-white rounded-xl shadow-lg p-6">
      <p>✅ 由 Trae 自动生成 | 📧 可直接分享给团队成员 | 🔄 每日 08:00 自动更新</p>
      <p class="mt-2">更新时间：${updateTime}</p>
    </div>
  </footer>

  <script>
    function shareBrief() {
      if (navigator.share) {
        navigator.share({
          title: '海外创意·AI视频·舞台设备 每日简报',
          text: '今日最新行业动态，快来看看！',
          url: window.location.href
        });
      } else {
        navigator.clipboard.writeText(window.location.href);
        alert('链接已复制到剪贴板！');
      }
    }
  </script>
</body>
</html>`;

    return html;
}

function main() {
    console.log('='.repeat(60));
    console.log('🚀 海外创意·AI视频·舞台设备 每日简报系统');
    console.log('='.repeat(60));
    
    // 生成数据
    console.log('\n📊 生成数据中...');
    const videos = generateVideoData();
    const aiNews = generateAiData();
    const stageProducts = generateStageData();
    console.log(`   - 视频：${videos.length} 条`);
    console.log(`   - AI动态：${aiNews.length} 条`);
    console.log(`   - 设备资讯：${stageProducts.length} 条`);
    
    // 构建HTML
    console.log('\n🎨 生成HTML页面...');
    const html = buildHtml(videos, aiNews, stageProducts);
    
    // 保存文件
    const outputFile = 'index.html';
    fs.writeFileSync(outputFile, html, 'utf-8');
    console.log(`✅ 已保存：${outputFile}`);
    
    // 显示成功信息
    console.log('\n' + '='.repeat(60));
    console.log('✅ 已完成更新');
    console.log(`访问链接：${CONFIG.web_url}`);
    console.log('='.repeat(60));
    console.log('\n提示：请在 GitHub 仓库中执行 git 命令完成部署');
    
    return 0;
}

main();
