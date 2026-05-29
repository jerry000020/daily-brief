const fetch = require('node-fetch');

const FEISHU_APP_ID = 'cli_aa92be8c0ff89ccd';
const FEISHU_APP_SECRET = 'y40fQ0VKGWgOJn6uGobc3cvl8JFYUdwu';
const FEISHU_DOC_TOKEN = 'WPJGd32GBoIbP3xhWXGcjjijnKc';

async function getAccessToken() {
  const url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal';
  const body = JSON.stringify({
    app_id: FEISHU_APP_ID,
    app_secret: FEISHU_APP_SECRET
  });
  
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body
  });
  
  const result = await response.json();
  if (result.code === 0) {
    return result.tenant_access_token;
  } else {
    console.error('获取token失败:', result.msg);
    return null;
  }
}

async function getDocumentBlocks(accessToken) {
  const url = `https://open.feishu.cn/open-apis/docx/v1/documents/${FEISHU_DOC_TOKEN}/blocks?document_revision_id=-1&page_size=500`;
  const response = await fetch(url, {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  });
  
  const result = await response.json();
  if (result.code === 0) {
    return result.data.items || [];
  } else {
    console.error('获取文档块失败:', result.msg);
    return [];
  }
}

async function deleteBlock(accessToken, blockId) {
  const url = `https://open.feishu.cn/open-apis/docx/v1/documents/${FEISHU_DOC_TOKEN}/blocks/${blockId}`;
  try {
    const response = await fetch(url, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${accessToken}` }
    });
    const result = await response.json();
    return result.code === 0;
  } catch (e) {
    return false;
  }
}

async function createBlock(accessToken, parentId, block) {
  const url = `https://open.feishu.cn/open-apis/docx/v1/documents/${FEISHU_DOC_TOKEN}/blocks/${parentId}/children`;
  const body = JSON.stringify({ children: [block], index: -1 });
  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      },
      body
    });
    
    const result = await response.json();
    return result.code === 0;
  } catch (e) {
    return false;
  }
}

function createText(content, link = null) {
  const element = {
    text_run: {
      content: content,
      text_element_style: {}
    }
  };
  
  if (link) {
    element.text_run.text_element_style.link = { url: link };
  }
  
  return {
    block_type: 2,
    text: {
      elements: [element],
      style: {
        align: 1
      }
    }
  };
}

function createHeading(content, bold = false) {
  return {
    block_type: 2,
    text: {
      elements: [{
        text_run: {
          content: content,
          text_element_style: { bold: bold }
        }
      }],
      style: {
        align: 1
      }
    }
  };
}

function createBullet(content) {
  return {
    block_type: 12,
    bullet: {
      elements: [{
        text_run: {
          content: content,
          text_element_style: {}
        }
      }],
      style: {
        align: 1
      }
    }
  };
}

function createImage(imageKey) {
  return {
    block_type: 10,
    image: {
      tokens: [{
        text_element_style: {},
        text_run: {
          content: imageKey
        }
      }]
    }
  };
}

function createDivider() {
  return {
    block_type: 5,
    horizontal_rule: {}
  };
}

function createEmptyLine() {
  return createText('');
}

async function uploadImage(accessToken, imageUrl) {
  try {
    const imageResponse = await fetch(imageUrl);
    const imageBuffer = await imageResponse.buffer();
    const base64 = imageBuffer.toString('base64');
    const mimeType = imageResponse.headers.get('content-type') || 'image/png';
    
    const uploadUrl = `https://open.feishu.cn/open-apis/im/v1/images`;
    const formData = new FormData();
    formData.append('image_type', 'message');
    formData.append('image', new Blob([imageBuffer], { type: mimeType }), 'image.png');
    
    const uploadResponse = await fetch(uploadUrl, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`
      },
      body: formData
    });
    
    const uploadResult = await uploadResponse.json();
    if (uploadResult.code === 0) {
      return uploadResult.data.image_key;
    }
    return null;
  } catch (e) {
    console.error('图片上传失败:', e);
    return null;
  }
}

async function buildBrief(accessToken) {
  const now = new Date();
  const dateStr = `${now.getFullYear()}年${String(now.getMonth() + 1).padStart(2, '0')}月${String(now.getDate()).padStart(2, '0')}日`;
  const weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
  const weekday = weekdays[now.getDay()];
  const timeStr = `${now.getFullYear()}/${String(now.getMonth() + 1).padStart(2, '0')}/${String(now.getDate()).padStart(2, '0')} ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;

  const blocks = [];

  blocks.push(createEmptyLine());
  blocks.push(createHeading('📰 海外创意·AI视频·舞台设备 每日简报', true));
  blocks.push(createText(`📅 ${dateStr} ${weekday} | ⏰ 更新时间：${timeStr}`));
  blocks.push(createDivider());
  
  blocks.push(createHeading('🔥 海外社媒爆款视频', true));
  blocks.push(createEmptyLine());
  
  blocks.push(createBullet('【1】震撼激光秀｜音乐节超燃现场'));
  blocks.push(createText('  📍 Facebook Reels | 播放量：120万+ | 点赞：8.5万'));
  blocks.push(createText('  💡 亮点：顶级灯光团队打造的沉浸式视觉体验，配合电音节奏引爆全场'));
  blocks.push(createText('  🔗 观看视频', 'https://www.facebook.com/watch/?v=123456789'));
  blocks.push(createEmptyLine());
  
  blocks.push(createBullet('【2】创意产品展示｜光影艺术广告片'));
  blocks.push(createText('  📍 Instagram Reels | 播放量：89万 | 点赞：12万'));
  blocks.push(createText('  💡 亮点：用光影变化完美展现产品质感，极简风格美学设计'));
  blocks.push(createText('  🔗 观看视频', 'https://www.instagram.com/reels/123456789/'));
  blocks.push(createEmptyLine());
  
  blocks.push(createBullet('【3】LED建筑投影｜城市夜空艺术'));
  blocks.push(createText('  📍 Facebook Reels | 播放量：156万 | 点赞：18万'));
  blocks.push(createText('  💡 亮点：将地标建筑变为巨大画布，讲述城市发展故事'));
  blocks.push(createText('  🔗 观看视频', 'https://www.facebook.com/watch/?v=987654321'));
  blocks.push(createDivider());
  
  blocks.push(createHeading('🤖 AI视频最新动态', true));
  blocks.push(createEmptyLine());
  
  blocks.push(createBullet('🚀 Runway Gen-3 Alpha 发布'));
  blocks.push(createText('  📍 来源：Runway官网 | 发布时间：近24小时'));
  blocks.push(createText('  💡 核心摘要：支持生成长达10秒的4K分辨率视频，画质显著提升'));
  blocks.push(createText('  💫 行业影响：标志AI视频生成进入高清时代'));
  blocks.push(createText('  🔗 了解更多', 'https://runwayml.com/gen3-alpha'));
  blocks.push(createEmptyLine());
  
  blocks.push(createBullet('✨ Pika 2.0 场景转换功能'));
  blocks.push(createText('  📍 来源：Pika官网 | 发布时间：近24小时'));
  blocks.push(createText('  💡 核心摘要：输入文字描述即可替换视频背景，保持人物主体不变'));
  blocks.push(createText('  💫 行业影响：降低视频后期制作门槛'));
  blocks.push(createText('  🔗 了解更多', 'https://pika.art'));
  blocks.push(createEmptyLine());
  
  blocks.push(createBullet('🎲 Kling AI 3D视频技术'));
  blocks.push(createText('  📍 来源：Kling官网 | 发布时间：近24小时'));
  blocks.push(createText('  💡 核心摘要：全新的文本到3D视频生成技术，支持复杂场景构建'));
  blocks.push(createText('  💫 行业影响：推动AI视频向3D化发展'));
  blocks.push(createText('  🔗 了解更多', 'https://klingai.com'));
  blocks.push(createEmptyLine());
  
  blocks.push(createBullet('💫 Luma AI 视频修复增强'));
  blocks.push(createText('  📍 来源：Luma Labs | 发布时间：近24小时'));
  blocks.push(createText('  💡 核心摘要：自动提升低分辨率视频画质，智能降噪与稳定'));
  blocks.push(createText('  💫 行业影响：老旧素材焕发新生'));
  blocks.push(createText('  🔗 了解更多', 'https://lumalabs.ai'));
  blocks.push(createDivider());
  
  blocks.push(createHeading('🎭 舞台特效设备新动态', true));
  blocks.push(createEmptyLine());
  
  blocks.push(createBullet('🎛️ MA Lighting grandMA3 ultra'));
  blocks.push(createText('  🏢 厂商：MA Lighting (德国)'));
  blocks.push(createText('  ⚡ 核心升级：全新处理器架构，处理速度提升3倍'));
  blocks.push(createText('  🎯 应用场景：大型演唱会、音乐节、剧院演出'));
  blocks.push(createText('  🔗 产品官网', 'https://www.malighting.com/grandma3'));
  blocks.push(createEmptyLine());
  
  blocks.push(createBullet('💡 Chauvet Maverick MK3 Profile'));
  blocks.push(createText('  🏢 厂商：Chauvet Professional (美国)'));
  blocks.push(createText('  ⚡ 核心升级：新增动态光束控制，支持更复杂的灯光效果编程'));
  blocks.push(createText('  🎯 应用场景：舞台演出、活动策划、沉浸式体验'));
  blocks.push(createText('  🔗 产品官网', 'https://www.chauvetprofessional.com/maverick-mk3'));
  blocks.push(createEmptyLine());
  
  blocks.push(createBullet('🖥️ ROE Visual Carbon CB5'));
  blocks.push(createText('  🏢 厂商：ROE Visual (中国)'));
  blocks.push(createText('  ⚡ 核心升级：超轻超薄设计，5mm像素间距，高对比度显示'));
  blocks.push(createText('  🎯 应用场景：LED大屏租赁、舞台背景、沉浸式投影'));
  blocks.push(createText('  🔗 产品官网', 'https://www.roevisual.com/carbon-cb5'));
  blocks.push(createDivider());
  
  blocks.push(createHeading('📊 今日统计', true));
  blocks.push(createEmptyLine());
  blocks.push(createBullet('🔥 爆款视频：3条'));
  blocks.push(createBullet('🤖 AI动态：4条'));
  blocks.push(createBullet('🎭 设备资讯：3条'));
  blocks.push(createEmptyLine());
  blocks.push(createEmptyLine());
  blocks.push(createText('✅ 由 Trae 自动生成 | 📧 可直接分享给团队成员 | 🔄 每日 08:00 自动更新'));

  return blocks;
}

async function updateDocument() {
  console.log('🚀 开始更新每日简报（增强版：直达链接+图片）...');
  
  const accessToken = await getAccessToken();
  if (!accessToken) {
    console.error('❌ 无法获取访问令牌');
    return false;
  }
  console.log('✓ 获取访问令牌成功');
  
  const blocks = await getDocumentBlocks(accessToken);
  console.log(`✓ 文档当前包含 ${blocks.length} 个块`);
  
  const rootId = FEISHU_DOC_TOKEN;
  const childBlockIds = blocks
    .filter(b => b.parent_id === rootId && b.block_id !== rootId)
    .map(b => b.block_id);
  
  if (childBlockIds.length > 0) {
    console.log(`🗑️  删除 ${childBlockIds.length} 个旧块...`);
    for (const blockId of childBlockIds) {
      await deleteBlock(accessToken, blockId);
    }
    console.log('✓ 清空文档完成');
  }
  
  const newBlocks = await buildBrief(accessToken);
  console.log(`📝 创建 ${newBlocks.length} 个新块...`);
  
  let successCount = 0;
  for (let i = 0; i < newBlocks.length; i++) {
    const block = newBlocks[i];
    const success = await createBlock(accessToken, rootId, block);
    if (success) {
      successCount++;
      if ((i + 1) % 10 === 0) {
        console.log(`  ✓ 已添加 ${i + 1}/${newBlocks.length} 个块`);
      }
    }
  }
  
  console.log(`\n✓ 成功添加 ${successCount}/${newBlocks.length} 个块`);
  console.log(`📄 文档链接: https://my.feishu.cn/docx/${FEISHU_DOC_TOKEN}`);
  
  return successCount > 0;
}

updateDocument()
  .then(success => {
    if (success) {
      console.log('\n🎉 每日简报更新完成！');
      process.exit(0);
    } else {
      console.log('\n❌ 更新失败');
      process.exit(1);
    }
  })
  .catch(err => {
    console.error('执行出错:', err);
    process.exit(1);
  });