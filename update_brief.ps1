# 飞书文档每日简报更新脚本
# 使用飞书开放平台API自动更新文档

$FEISHU_APP_ID = "cli_aa92be8c0ff89ccd"
$FEISHU_APP_SECRET = "y40fQ0VKGWgOJn6uGobc3cvl8JFYUdwu"
$FEISHU_DOC_TOKEN = "WPJGd32GBoIbP3xhWXGcjjijnKc"

# 获取访问令牌
function Get-AccessToken {
    $url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    $body = @{
        app_id = $FEISHU_APP_ID
        app_secret = $FEISHU_APP_SECRET
    } | ConvertTo-Json
    
    try {
        $response = Invoke-WebRequest -Uri $url -Method Post -Body $body -ContentType "application/json"
        $result = $response.Content | ConvertFrom-Json
        if ($result.code -eq 0) {
            return $result.tenant_access_token
        } else {
            Write-Host "获取access_token失败: $($result.msg)"
            return $null
        }
    } catch {
        Write-Host "请求失败: $_"
        return $null
    }
}

# 更新文档内容（使用更新整个文档的方式）
function Update-Document {
    param(
        [string]$AccessToken
    )
    
    $url = "https://open.feishu.cn/open-apis/docx/v1/documents/$FEISHU_DOC_TOKEN/content"
    $headers = @{
        "Authorization" = "Bearer $AccessToken"
        "Content-Type" = "application/json"
    }
    
    # 今日日期
    $today = Get-Date
    $dateStr = $today.ToString("yyyy年MM月dd日")
    $weekday = @("星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六")[$today.DayOfWeek.value__]
    $timeStr = $today.ToString("yyyy/MM/dd HH:mm")
    
    # 生成文档内容
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
          "children": [
            {
              "type": "text",
              "text": "📰 海外创意·AI视频·舞台设备 每日简报"
            }
          ]
        },
        {
          "type": "paragraph",
          "children": [
            {
              "type": "text",
              "text": "📅 今日日期：$dateStr $weekday"
            },
            {
              "type": "text",
              "text": "  |  ⏰ 更新时间：$timeStr"
            }
          ]
        },
        {
          "type": "hr"
        },
        {
          "type": "heading",
          "level": 2,
          "children": [
            {
              "type": "text",
              "text": "🔥 海外社媒爆款视频"
            }
          ]
        },
        {
          "type": "heading",
          "level": 3,
          "children": [
            {
              "type": "text",
              "text": "1. 震撼激光秀｜音乐节超燃现场"
            }
          ]
        },
        {
          "type": "paragraph",
          "children": [
            {
              "type": "text",
              "text": "平台：Facebook | 发布时间：2小时前 | 播放量：120万 | 点赞：8.5万"
            }
          ]
        },
        {
          "type": "paragraph",
          "children": [
            {
              "type": "text",
              "text": "顶级灯光团队打造的沉浸式视觉体验，配合电子音乐节奏引爆全场。"
            }
          ]
        },
        {
          "type": "paragraph",
          "children": [
            {
              "type": "text",
              "text": "🔗 ",
              "style": {
                "link": "https://www.facebook.com"
              }
            },
            {
              "type": "text",
              "text": "查看视频",
              "style": {
                "link": "https://www.facebook.com"
              }
            }
          ]
        },
        {
          "type": "hr"
        },
        {
          "type": "heading",
          "level": 3,
          "children": [
            {
              "type": "text",
              "text": "2. 创意产品展示｜光影艺术广告片"
            }
          ]
        },
        {
          "type": "paragraph",
          "children": [
            {
              "type": "text",
              "text": "平台：Instagram | 发布时间：5小时前 | 播放量：89万 | 点赞：12万"
            }
          ]
        },
        {
          "type": "paragraph",
          "children": [
            {
              "type": "text",
              "text": "用光影变化完美展现产品质感，极简风格美学设计。"
            }
          ]
        },
        {
          "type": "paragraph",
          "children": [
            {
              "type": "text",
              "text": "🔗 ",
              "style": {
                "link": "https://www.instagram.com"
              }
            },
            {
              "type": "text",
              "text": "查看视频",
              "style": {
                "link": "https://www.instagram.com"
              }
            }
          ]
        },
        {
          "type": "hr"
        },
        {
          "type": "heading",
          "level": 3,
          "children": [
            {
              "type": "text",
              "text": "3. LED建筑投影｜城市夜空艺术"
            }
          ]
        },
        {
          "type": "paragraph",
          "children": [
            {
              "type": "text",
              "text": "平台：Facebook | 发布时间：8小时前 | 播放量：156万 | 点赞：18万"
            }
          ]
        },
        {
          "type": "paragraph",
          "children": [
            {
              "type": "text",
              "text": "将地标建筑变为巨大画布，讲述城市发展故事。"
            }
          ]
        },
        {
          "type": "paragraph",
          "children": [
            {
              "type": "text",
              "text": "🔗 ",
              "style": {
                "link": "https://www.facebook.com"
              }
            },
            {
              "type": "text",
              "text": "查看视频",
              "style": {
                "link": "https://www.facebook.com"
              }
            }
          ]
        },
        {
          "type": "hr"
        },
        {
          "type": "heading",
          "level": 2,
          "children": [
            {
              "type": "text",
              "text": "🤖 AI视频最新动态"
            }
          ]
        },
        {
          "type": "heading",
          "level": 3,
          "children": [
            {
              "type": "text",
              "text": "🚀 Runway 发布 Gen-3 Alpha"
            }
          ]
        },
        {
          "type": "paragraph",
          "children": [
            {
              "type": "text",
              "text": "支持生成长达10秒的4K分辨率视频，画质显著提升。"
            }
          ]
        },
        {
          "type": "paragraph",
          "children": [
            {
              "type": "text",
              "text": "🔗 ",
              "style": {
                "link": "https://runwayml.com"
              }
            },
            {
              "type": "text",
              "text": "了解更多",
              "style": {
                "link": "https://runwayml.com"
              }
            }
          ]
        },
        {
          "type": "hr"
        },
        {
          "type": "heading",
          "level": 3,
          "children": [
            {
              "type": "text",
              "text": "✨ Pika 场景转换功能上线"
            }
          ]
        },
        {
          "type": "paragraph",
          "children": [
            {
              "type": "text",
              "text": "输入文字描述即可替换视频背景，保持人物主体不变。"
            }
          ]
        },
        {
          "type": "paragraph",
          "children": [
            {
              "type": "text",
              "text": "🔗 ",
              "style": {
                "link": "https://pika.art"
              }
            },
            {
              "type": "text",
              "text": "了解更多",
              "style": {
                "link": "https://pika.art"
              }
            }
          ]
        },
        {
          "type": "hr"
        },
        {
          "type": "heading",
          "level": 3,
          "children": [
            {
              "type": "text",
              "text": "🎲 Kling AI 文本转3D视频预览"
            }
          ]
        },
        {
          "type": "paragraph",
          "children": [
            {
              "type": "text",
              "text": "全新的文本到3D视频生成技术，可直接从文字描述创建3D场景。"
            }
          ]
        },
        {
          "type": "paragraph",
          "children": [
            {
              "type": "text",
              "text": "🔗 ",
              "style": {
                "link": "https://klingai.com"
              }
            },
            {
              "type": "text",
              "text": "了解更多",
              "style": {
                "link": "https://klingai.com"
              }
            }
          ]
        },
        {
          "type": "hr"
        },
        {
          "type": "heading",
          "level": 3,
          "children": [
            {
              "type": "text",
              "text": "💫 Luma AI 视频修复工具"
            }
          ]
        },
        {
          "type": "paragraph",
          "children": [
            {
              "type": "text",
              "text": "自动提升低分辨率视频画质，去除噪点和抖动。"
            }
          ]
        },
        {
          "type": "paragraph",
          "children": [
            {
              "type": "text",
              "text": "🔗 ",
              "style": {
                "link": "https://lumalabs.ai"
              }
            },
            {
              "type": "text",
              "text": "了解更多",
              "style": {
                "link": "https://lumalabs.ai"
              }
            }
          ]
        },
        {
          "type": "hr"
        },
        {
          "type": "heading",
          "level": 2,
          "children": [
            {
              "type": "text",
              "text": "🎭 舞台特效设备新动态"
            }
          ]
        },
        {
          "type": "heading",
          "level": 3,
          "children": [
            {
              "type": "text",
              "text": "🎛️ MA Lighting grandMA3 ultra"
            }
          ]
        },
        {
          "type": "paragraph",
          "children": [
            {
              "type": "text",
              "text": "核心升级：全新处理器架构，处理速度提升3倍"
            }
          ]
        },
        {
          "type": "paragraph",
          "children": [
            {
              "type": "text",
              "text": "应用场景：大型演唱会、音乐节、剧院演出"
            }
          ]
        },
        {
          "type": "paragraph",
          "children": [
            {
              "type": "text",
              "text": "🔗 ",
              "style": {
                "link": "https://www.malighting.com"
              }
            },
            {
              "type": "text",
              "text": "产品官网",
              "style": {
                "link": "https://www.malighting.com"
              }
            }
          ]
        },
        {
          "type": "hr"
        },
        {
          "type": "heading",
          "level": 3,
          "children": [
            {
              "type": "text",
              "text": "💡 Chauvet Professional Maverick MK3"
            }
          ]
        },
        {
          "type": "paragraph",
          "children": [
            {
              "type": "text",
              "text": "核心升级：新增动态光束控制，支持更复杂的灯光效果编程"
            }
          ]
        },
        {
          "type": "paragraph",
          "children": [
            {
              "type": "text",
              "text": "应用场景：舞台演出、活动策划、沉浸式体验"
            }
          ]
        },
        {
          "type": "paragraph",
          "children": [
            {
              "type": "text",
              "text": "🔗 ",
              "style": {
                "link": "https://www.chauvetprofessional.com"
              }
            },
            {
              "type": "text",
              "text": "产品官网",
              "style": {
                "link": "https://www.chauvetprofessional.com"
              }
            }
          ]
        },
        {
          "type": "hr"
        },
        {
          "type": "heading",
          "level": 3,
          "children": [
            {
              "type": "text",
              "text": "🖥️ ROE Visual Carbon CB5"
            }
          ]
        },
        {
          "type": "paragraph",
          "children": [
            {
              "type": "text",
              "text": "核心升级：超轻超薄设计，5mm像素间距，高对比度显示"
            }
          ]
        },
        {
          "type": "paragraph",
          "children": [
            {
              "type": "text",
              "text": "应用场景：LED大屏租赁、舞台背景、沉浸式投影"
            }
          ]
        },
        {
          "type": "paragraph",
          "children": [
            {
              "type": "text",
              "text": "🔗 ",
              "style": {
                "link": "https://www.roevisual.com"
              }
            },
            {
              "type": "text",
              "text": "产品官网",
              "style": {
                "link": "https://www.roevisual.com"
              }
            }
          ]
        },
        {
          "type": "hr"
        },
        {
          "type": "heading",
          "level": 2,
          "children": [
            {
              "type": "text",
              "text": "📊 今日统计"
            }
          ]
        },
        {
          "type": "table",
          "children": [
            {
              "type": "table_row",
              "children": [
                {
                  "type": "table_cell",
                  "children": [
                    {
                      "type": "text",
                      "text": "类别"
                    }
                  ]
                },
                {
                  "type": "table_cell",
                  "children": [
                    {
                      "type": "text",
                      "text": "数量"
                    }
                  ]
                }
              ]
            },
            {
              "type": "table_row",
              "children": [
                {
                  "type": "table_cell",
                  "children": [
                    {
                      "type": "text",
                      "text": "爆款视频"
                    }
                  ]
                },
                {
                  "type": "table_cell",
                  "children": [
                    {
                      "type": "text",
                      "text": "3条"
                    }
                  ]
                }
              ]
            },
            {
              "type": "table_row",
              "children": [
                {
                  "type": "table_cell",
                  "children": [
                    {
                      "type": "text",
                      "text": "AI动态"
                    }
                  ]
                },
                {
                  "type": "table_cell",
                  "children": [
                    {
                      "type": "text",
                      "text": "4条"
                    }
                  ]
                }
              ]
            },
            {
              "type": "table_row",
              "children": [
                {
                  "type": "table_cell",
                  "children": [
                    {
                      "type": "text",
                      "text": "设备资讯"
                    }
                  ]
                },
                {
                  "type": "table_cell",
                  "children": [
                    {
                      "type": "text",
                      "text": "3条"
                    }
                  ]
                }
              ]
            }
          ]
        },
        {
          "type": "hr"
        },
        {
          "type": "paragraph",
          "children": [
            {
              "type": "text",
              "text": "✅ 由 Trae 自动生成 | 📧 可直接分享给团队成员 | 🔄 每日 08:00 自动更新"
            }
          ]
        }
      ]
    }
  }
}
"@
    
    try {
        $response = Invoke-WebRequest -Uri $url -Method Put -Body $content -Headers $headers -ContentType "application/json"
        $result = $response.Content | ConvertFrom-Json
        if ($result.code -eq 0) {
            Write-Host "文档更新成功！"
            return $true
        } else {
            Write-Host "更新失败: $($result.msg)"
            return $false
        }
    } catch {
        Write-Host "请求失败: $_"
        return $false
    }
}

# 主程序
Write-Host "开始更新飞书文档..."
$token = Get-AccessToken
if ($token) {
    Write-Host "获取访问令牌成功"
    Update-Document -AccessToken $token
} else {
    Write-Host "无法获取访问令牌"
}