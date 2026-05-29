const fetch = require('node-fetch');

async function test() {
  const token = 't-g1045shUMLPR4I6V6FTRY3CGTLNWN5CNQLC5F2K2';
  const docToken = 'WPJGd32GBoIbP3xhWXGcjjijnKc';
  
  const url = `https://open.feishu.cn/open-apis/docx/v1/documents/${docToken}/blocks/${docToken}/children`;
  const body = JSON.stringify({
    children: [{
      block_type: 6,
      text: {
        elements: [{
          text_run: {
            content: '测试段落',
            text_element_style: {}
          }
        }],
        style: {}
      }
    }]
  });
  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: body
    });
    
    const result = await response.text();
    console.log('响应:', result);
  } catch (error) {
    console.error('错误:', error.message);
  }
}

test();