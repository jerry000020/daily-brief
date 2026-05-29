const fetch = require('node-fetch');

async function testSimpleParagraph() {
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
  
  const docToken = 'WPJGd32GBoIbP3xhWXGcjjijnKc';
  
  const url = `https://open.feishu.cn/open-apis/docx/v1/documents/${docToken}/blocks/${docToken}/children`;
  const body = {
    children: [{
      block_type: 2,
      text: {
        elements: [{
          text_run: {
            content: "✅ 测试成功！飞书API现在可以正常工作了！",
            text_element_style: {}
          }
        }],
        style: {
          align: 1
        }
      }
    }],
    index: -1
  };
  
  console.log('发送请求...');
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(body)
  });
  
  const result = await response.json();
  console.log('响应:', JSON.stringify(result, null, 2));
}

testSimpleParagraph();