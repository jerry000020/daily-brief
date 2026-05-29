# Simple Feishu Document Update Script
# This script uses the blocks API to update the document

$FEISHU_APP_ID = "cli_aa92be8c0ff89ccd"
$FEISHU_APP_SECRET = "y40fQ0VKGWgOJn6uGobc3cvl8JFYUdwu"
$FEISHU_DOC_TOKEN = "WPJGd32GBoIbP3xhWXGcjjijnKc"

Write-Host "=== Feishu Daily Brief Update ===" -ForegroundColor Cyan

# Step 1: Get Access Token
Write-Host "1. Getting access token..." -ForegroundColor Yellow
try {
    $tokenUrl = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    $tokenBody = @{
        app_id = $FEISHU_APP_ID
        app_secret = $FEISHU_APP_SECRET
    } | ConvertTo-Json

    $tokenResponse = Invoke-WebRequest -Uri $tokenUrl -Method Post -Body $tokenBody -ContentType "application/json"
    $tokenResult = $tokenResponse.Content | ConvertFrom-Json

    if ($tokenResult.code -eq 0) {
        $accessToken = $tokenResult.tenant_access_token
        Write-Host "   Success! Token obtained: $($accessToken.Substring(0, 20))..." -ForegroundColor Green
    } else {
        Write-Host "   Failed to get token: $($tokenResult.msg)" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "   Error: $_" -ForegroundColor Red
    exit 1
}

# Step 2: Get Current Document Blocks
Write-Host "2. Getting document blocks..." -ForegroundColor Yellow
try {
    $blocksUrl = "https://open.feishu.cn/open-apis/docx/v1/documents/$FEISHU_DOC_TOKEN/blocks?document_revision_id=-1&page_size=500"
    $headers = @{
        "Authorization" = "Bearer $accessToken"
    }

    $blocksResponse = Invoke-WebRequest -Uri $blocksUrl -Headers $headers
    $blocksResult = $blocksResponse.Content | ConvertFrom-Json

    if ($blocksResult.code -eq 0) {
        $blocks = $blocksResult.data.items
        Write-Host "   Success! Found $($blocks.Count) blocks" -ForegroundColor Green
    } else {
        Write-Host "   Failed to get blocks: $($blocksResult.msg)" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "   Error: $_" -ForegroundColor Red
    exit 1
}

# Step 3: Delete Existing Child Blocks
Write-Host "3. Deleting existing blocks..." -ForegroundColor Yellow
$childBlockIds = @()
foreach ($block in $blocks) {
    if ($block.parent_id -eq $FEISHU_DOC_TOKEN -and $block.block_id -ne $FEISHU_DOC_TOKEN) {
        $childBlockIds += $block.block_id
    }
}

if ($childBlockIds.Count -gt 0) {
    $deletedCount = 0
    foreach ($blockId in $childBlockIds) {
        try {
            $deleteUrl = "https://open.feishu.cn/open-apis/docx/v1/documents/$FEISHU_DOC_TOKEN/blocks/$blockId"
            Invoke-WebRequest -Uri $deleteUrl -Method Delete -Headers $headers | Out-Null
            $deletedCount++
        } catch {
            Write-Host "   Warning: Could not delete block $blockId" -ForegroundColor Yellow
        }
    }
    Write-Host "   Deleted $deletedCount blocks" -ForegroundColor Green
} else {
    Write-Host "   No blocks to delete" -ForegroundColor Gray
}

# Step 4: Create New Content Blocks
Write-Host "4. Creating new content..." -ForegroundColor Yellow

$today = Get-Date
$dateStr = $today.ToString("yyyy年MM月dd日")
$timeStr = $today.ToString("yyyy/MM/dd HH:mm")
$weekdays = @("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
$weekday = $weekdays[$today.DayOfWeek.value__]

# Function to create a text block
function New-TextBlock {
    param([string]$text, [bool]$bold = $false)
    
    $elements = @(@{
        text_run = @{
            content = $text
            text_element_style = if ($bold) { @{ bold = $true } } else { @{} }
        }
    })
    
    return @{
        block_type = 2
        text = @{
            elements = $elements
            style = @{ align = 1 }
        }
    }
}

# Function to create a bullet point block
function New-BulletBlock {
    param([string]$text)
    
    $elements = @(@{
        text_run = @{
            content = $text
            text_element_style = @{}
        }
    })
    
    return @{
        block_type = 12
        bullet = @{
            elements = $elements
            style = @{ align = 1 }
        }
    }
}

# Function to create a divider
function New-DividerBlock {
    return @{
        block_type = 5
        horizontal_rule = @{}
    }
}

# Build the content blocks
$newBlocks = @()
$newBlocks += New-TextBlock -text ""
$newBlocks += New-TextBlock -text "Daily Brief - $dateStr $weekday" -bold $true
$newBlocks += New-TextBlock -text "Updated: $timeStr"
$newBlocks += New-DividerBlock
$newBlocks += New-TextBlock -text "Top News:" -bold $true
$newBlocks += New-BulletBlock -text "Runway released Gen-3 Alpha (4K video)"
$newBlocks += New-BulletBlock -text "Pika launched scene transition feature"
$newBlocks += New-BulletBlock -text "Kling AI previewed text-to-3D video"
$newBlocks += New-TextBlock -text ""
$newBlocks += New-TextBlock -text "This document was automatically updated."

# Add the blocks to the document
$successCount = 0
foreach ($block in $newBlocks) {
    try {
        $createUrl = "https://open.feishu.cn/open-apis/docx/v1/documents/$FEISHU_DOC_TOKEN/blocks/$FEISHU_DOC_TOKEN/children"
        $createBody = @{
            children = @($block)
            index = -1
        } | ConvertTo-Json -Depth 10

        $createResponse = Invoke-WebRequest -Uri $createUrl -Method Post -Body $createBody -Headers $headers -ContentType "application/json"
        $createResult = $createResponse.Content | ConvertFrom-Json

        if ($createResult.code -eq 0) {
            $successCount++
        }
    } catch {
        Write-Host "   Warning: Could not create block" -ForegroundColor Yellow
    }
}

Write-Host "   Created $successCount/$($newBlocks.Count) blocks" -ForegroundColor Green

# Done
Write-Host ""
Write-Host "=== Update Complete ===" -ForegroundColor Cyan
Write-Host "Document URL: https://my.feishu.cn/docx/$FEISHU_DOC_TOKEN" -ForegroundColor Blue
Write-Host ""
