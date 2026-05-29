const fetch = require('node-fetch');

async function checkExistingBlocks() {
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
  
  const url = `https://open.feishu.cn/open-apis/docx/v1/documents/${docToken}/blocks?document_revision_id=-1&page_size=5`;
  const response = await fetch(url, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  
  const result = await response.json();
  console.log('现有块结构:');
  console.log(JSON.stringify(result.data.items, null, 2));
}

checkExistingBlocks();