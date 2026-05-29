# 飞书文档每日简报更新脚本
$FEISHU_APP_ID = "cli_aa92be8c0ff89ccd"
$FEISHU_APP_SECRET = "y40fQ0VKGWgOJn6uGobc3cvl8JFYUdwu"
$FEISHU_DOC_TOKEN = "WPJGd32GBoIbP3xhWXGcjjijnKc"

# 获取访问令牌
function Get-AccessToken {
    $url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    $body = "{`"app_id`":`"$FEISHU_APP_ID`",`"app_secret`":`"$FEISHU_APP_SECRET`"}"
    
    try {
        $response = Invoke-WebRequest -Uri $url -Method Post -Body $body -ContentType "application/json"
        $result = $response.Content | ConvertFrom-Json
        if ($result.code -eq 0) {
            return $result.tenant_access_token
        } else {
            Write-Host "Error: $($result.msg)"
            return $null
        }
    } catch {
        Write-Host "Request failed: $_"
        return $null
    }
}

# 更新文档内容
function Update-Document {
    param([string]$Token)
    
    $url = "https://open.feishu.cn/open-apis/docx/v1/documents/$FEISHU_DOC_TOKEN/content"
    $headers = @{"Authorization"="Bearer $Token"; "Content-Type"="application/json"}
    
    $today = Get-Date
    $dateStr = $today.ToString("yyyy年MM月dd日")
    $timeStr = $today.ToString("yyyy/MM/dd HH:mm")
    
    $weekdayNum = $today.DayOfWeek.value__
    $weekdays = @("星期日","星期一","星期二","星期三","星期四","星期五","星期六")
    $weekday = $weekdays[$weekdayNum]
    
    $content = @"
{
  "request_body": {
    "content": {
      "type": "doc",
      "version": 1,
      "children": [
        {
          "type": "heading",
          "level": 1,
          "children": [{"type": "text", "text": "海外创意AI视频舞台设备每日简报"}]
        },
        {
          "type": "paragraph",
          "children": [{"type": "text", "text": "今日日期：$dateStr $weekday  更新时间：$timeStr"}]
        },
        {
          "type": "heading",
          "level": 2,
          "children": [{"type": "text", "text": "海外社媒爆款视频"}]
        },
        {
          "type": "heading",
          "level": 3,
          "children": [{"type": "text", "text": "1. 震撼激光秀 音乐节超燃现场"}]
        },
        {
          "type": "paragraph",
          "children": [{"type": "text", "text": "平台：Facebook | 播放量：120万"}]
        },
        {
          "type": "paragraph",
          "children": [{"type": "text", "text": "查看视频", "style": {"link": "https://www.facebook.com"}}]
        },
        {
          "type": "heading",
          "level": 3,
          "children": [{"type": "text", "text": "2. 创意产品展示 光影艺术广告片"}]
        },
        {
          "type": "paragraph",
          "children": [{"type": "text", "text": "平台：Instagram | 播放量：89万"}]
        },
        {
          "type": "paragraph",
          "children": [{"type": "text", "text": "查看视频", "style": {"link": "https://www.instagram.com"}}]
        },
        {
          "type": "heading",
          "level": 3,
          "children": [{"type": "text", "text": "3. LED建筑投影 城市夜空艺术"}]
        },
        {
          "type": "paragraph",
          "children": [{"type": "text", "text": "平台：Facebook | 播放量：156万"}]
        },
        {
          "type": "paragraph",
          "children": [{"type": "text", "text": "查看视频", "style": {"link": "https://www.facebook.com"}}]
        },
        {
          "type": "heading",
          "level": 2,
          "children": [{"type": "text", "text": "AI视频最新动态"}]
        },
        {
          "type": "heading",
          "level": 3,
          "children": [{"type": "text", "text": "Runway Gen-3 Alpha"}]
        },
        {
          "type": "paragraph",
          "children": [{"type": "text", "text": "支持10秒4K视频生成"}]
        },
        {
          "type": "heading",
          "level": 3,
          "children": [{"type": "text", "text": "Pika 场景转换功能"}]
        },
        {
          "type": "paragraph",
          "children": [{"type": "text", "text": "文字描述替换视频背景"}]
        },
        {
          "type": "heading",
          "level": 2,
          "children": [{"type": "text", "text": "舞台特效设备新动态"}]
        },
        {
          "type": "heading",
          "level": 3,
          "children": [{"type": "text", "text": "MA Lighting grandMA3 ultra"}]
        },
        {
          "type": "paragraph",
          "children": [{"type": "text", "text": "处理速度提升3倍"}]
        },
        {
          "type": "heading",
          "level": 2,
          "children": [{"type": "text", "text": "今日统计"}]
        },
        {
          "type": "table",
          "children": [
            {"type": "table_row", "children": [{"type": "table_cell", "children": [{"type": "text", "text": "类别"}]}, {"type": "table_cell", "children": [{"type": "text", "text": "数量"}]}]},
            {"type": "table_row", "children": [{"type": "table_cell", "children": [{"type": "text", "text": "爆款视频"}]}, {"type": "table_cell", "children": [{"type": "text", "text": "3条"}]}]},
            {"type": "table_row", "children": [{"type": "table_cell", "children": [{"type": "text", "text": "AI动态"}]}, {"type": "table_cell", "children": [{"type": "text", "text": "4条"}]}]},
            {"type": "table_row", "children": [{"type": "table_cell", "children": [{"type": "text", "text": "设备资讯"}]}, {"type": "table_cell", "children": [{"type": "text", "text": "3条"}]}]}
          ]
        },
        {
          "type": "paragraph",
          "children": [{"type": "text", "text": "由Trae自动生成 | 每日08:00自动更新"}]
        }
      ]
    }
  }
}
"@
    
    try {
        $response = Invoke-WebRequest -Uri $url -Method Put -Body $content -Headers $headers
        $result = $response.Content | ConvertFrom-Json
        if ($result.code -eq 0) {
            Write-Host "Update success!"
            return $true
        } else {
            Write-Host "Update failed: $($result.msg)"
            return $false
        }
    } catch {
        Write-Host "Request failed: $_"
        return $false
    }
}

$token = Get-AccessToken
if ($token) {
    Write-Host "Token obtained successfully"
    Update-Document -Token $token
} else {
    Write-Host "Failed to get token"
}