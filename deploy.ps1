# GitHub 自动部署脚本
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "🚀 每日简报系统 - GitHub 部署脚本" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

# 检查 git 是否存在
try {
    git --version | Out-Null
} catch {
    Write-Host "❌ Git 未安装，请先安装 Git" -ForegroundColor Red
    exit 1
}

# 运行主脚本生成 index.html
Write-Host "`n📊 生成最新简报..." -ForegroundColor Yellow
python main.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 生成失败" -ForegroundColor Red
    exit 1
}

# 检查 git 仓库状态
Write-Host "`n📦 检查 Git 状态..." -ForegroundColor Yellow
git status

Write-Host "`n🔄 提交更改..." -ForegroundColor Yellow
git add .
git commit -m "每日简报自动更新 - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"

Write-Host "`n🚀 推送到 GitHub..." -ForegroundColor Yellow
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n" + "=" * 60 -ForegroundColor Green
    Write-Host "✅ 已完成更新" -ForegroundColor Green
    Write-Host "访问链接：https://jerry000020.github.io/daily-brief/" -ForegroundColor Green
    Write-Host "=" * 60 -ForegroundColor Green
} else {
    Write-Host "`n❌ 推送失败，请检查网络或 Git 配置" -ForegroundColor Red
    exit 1
}
