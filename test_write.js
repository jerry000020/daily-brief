const fetch = require('node-fetch');

async function testWriteAPI() {
  // 获取token
  const authResponse = await fetch('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      app_id: 'cli_aa92be8c0ff89ccd',
      app_secret: 'y40fQ0VKGWgOJn6uGobc3cvl8JFYUdwu'
    })
  });
  const authData = await authResponse.json();
  const token = authData.tenant_access_token;
  console.log('✓ 获取Token成功');

  const docToken = 'WPJGd32GBoIbP3xhWXGcjjijnKc';

  // 测试创建段落
  const url = `https://open.feishu.cn/open-apis/docx/v1/documents/${docToken}/blocks/${docToken}/children`;
  
  const blockData = {
    children: [{
      block_type: 2,
      heading1: {
        elements: [{
          text_run: {
            content: '📰 海外创意·AI视频·舞台设备 每日简报',
            text_element_style: {}
          }
        }],
        style: {}
      }
    }],
    index: 0
  };

  console.log('发送请求到:', url);
  console.log('请求体:', JSON.stringify(blockData, null, 2));

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(blockData)
  });

  const result = await response.json();
  console.log('响应:', JSON.stringify(result, null, 2));
  
  return result.code === 0;
}

testWriteAPI()
  .then(success => {
    console.log('\n' + (success ? '✅ 写入API测试成功！' : '❌ 写入API测试失败'));
    process.exit(success ? 0 : 1);
  })
  .catch(err => {
    console.error('错误:', err);
    process.exit(1);
  });