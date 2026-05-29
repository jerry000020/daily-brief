const fetch = require('node-fetch');

async function checkAllBlocks() {
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
  
  const url = `https://open.feishu.cn/open-apis/docx/v1/documents/${docToken}/blocks?document_revision_id=-1&page_size=100`;
  const response = await fetch(url, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  
  const result = await response.json();
  console.log('所有块:');
  result.data.items.forEach((item, idx) => {
    console.log(`${idx + 1}. block_id: ${item.block_id}, block_type: ${item.block_type}`);
    if (item.text) console.log('   text:', item.text.elements[0].text_run.content.substring(0, 30));
    if (item.heading1) console.log('   heading1:', item.heading1.elements[0].text_run.content.substring(0, 30));
    if (item.heading2) console.log('   heading2:', item.heading2.elements[0].text_run.content.substring(0, 30));
    if (item.heading3) console.log('   heading3:', item.heading3.elements[0].text_run.content.substring(0, 30));
    if (item.bullet) console.log('   bullet:', item.bullet.elements[0].text_run.content.substring(0, 30));
  });
}

checkAllBlocks();