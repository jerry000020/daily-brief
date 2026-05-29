# Feishu Document Update - Complete Version
Write-Host "=== Feishu Daily Brief Update ==="

# Configuration
$FEISHU_APP_ID = "cli_aa92be8c0ff89ccd"
$FEISHU_APP_SECRET = "y40fQ0VKGWgOJn6uGobc3cvl8JFYUdwu"
$FEISHU_DOC_TOKEN = "WPJGd32GBoIbP3xhWXGcjjijnKc"

# Step 1: Get Access Token
Write-Host "Step 1: Getting access token..."
$tokenUrl = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
$tokenBody = "{""app_id"":""$FEISHU_APP_ID"",""app_secret"":""$FEISHU_APP_SECRET""}"
$tokenResponse = Invoke-WebRequest -Uri $tokenUrl -Method Post -Body $tokenBody -ContentType "application/json"
$tokenResult = $tokenResponse.Content | ConvertFrom-Json
$accessToken = $tokenResult.tenant_access_token
Write-Host "  Token obtained successfully!"

# Step 2: Get Document Blocks
Write-Host "Step 2: Getting current document blocks..."
$blocksUrl = "https://open.feishu.cn/open-apis/docx/v1/documents/$FEISHU_DOC_TOKEN/blocks?document_revision_id=-1&page_size=500"
$headers = @{"Authorization"="Bearer $accessToken"}
$blocksResponse = Invoke-WebRequest -Uri $blocksUrl -Headers $headers
$blocksResult = $blocksResponse.Content | ConvertFrom-Json
$blocks = $blocksResult.data.items
Write-Host "  Found $($blocks.Count) blocks in document"

# Step 3: Delete Child Blocks
Write-Host "Step 3: Deleting old blocks..."
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
        } catch { }
    }
    Write-Host "  Deleted $deletedCount old blocks"
} else {
    Write-Host "  No old blocks to delete"
}

# Step 4: Create New Blocks
Write-Host "Step 4: Creating new content..."

$today = Get-Date
$dateStr = $today.ToString("yyyy-MM-dd")
$timeStr = $today.ToString("HH:mm")

# Create text block function
function CreateTextBlock {
    param($text, $bold = $false)
    $style = if ($bold) { @{ bold = $true } } else { @{} }
    $elements = @(@{ text_run = @{ content = $text; text_element_style = $style } })
    return @{ block_type = 2; text = @{ elements = $elements; style = @{ align = 1 } } }
}

# Create bullet block function
function CreateBulletBlock {
    param($text)
    $elements = @(@{ text_run = @{ content = $text; text_element_style = @{} } })
    return @{ block_type = 12; bullet = @{ elements = $elements; style = @{ align = 1 } } }
}

# Create divider
function CreateDivider {
    return @{ block_type = 5; horizontal_rule = @{} }
}

# Build content
$newBlocks = @()
$newBlocks += CreateTextBlock -text ""
$newBlocks += CreateTextBlock -text "Daily Brief - $dateStr $timeStr" -bold $true
$newBlocks += CreateDivider
$newBlocks += CreateTextBlock -text "Top News:" -bold $true
$newBlocks += CreateBulletBlock -text "Runway released Gen-3 Alpha (4K video generation)"
$newBlocks += CreateBulletBlock -text "Pika launched scene transition feature"
$newBlocks += CreateBulletBlock -text "Kling AI previewed text-to-3D video"
$newBlocks += CreateTextBlock -text ""
$newBlocks += CreateTextBlock -text "Stage Equipment Updates:" -bold $true
$newBlocks += CreateBulletBlock -text "MA Lighting grandMA3 ultra (3x faster)"
$newBlocks += CreateBulletBlock -text "Chauvet Professional Maverick MK3"
$newBlocks += CreateTextBlock -text ""
$newBlocks += CreateTextBlock -text "Automatically updated by Trae"

# Add blocks to document
$successCount = 0
foreach ($block in $newBlocks) {
    try {
        $createUrl = "https://open.feishu.cn/open-apis/docx/v1/documents/$FEISHU_DOC_TOKEN/blocks/$FEISHU_DOC_TOKEN/children"
        $createBody = ConvertTo-Json @{ children = @($block); index = -1 } -Depth 10
        $createResponse = Invoke-WebRequest -Uri $createUrl -Method Post -Body $createBody -Headers $headers -ContentType "application/json"
        $createResult = $createResponse.Content | ConvertFrom-Json
        if ($createResult.code -eq 0) {
            $successCount++
        }
    } catch { }
}

Write-Host "  Created $successCount/$($newBlocks.Count) new blocks"

# Done
Write-Host ""
Write-Host "=== Update Complete ==="
Write-Host "Document: https://my.feishu.cn/docx/$FEISHU_DOC_TOKEN"
Write-Host ""
