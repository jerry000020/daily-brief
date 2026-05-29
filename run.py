#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主运行脚本：抓取数据 → 生成HTML → 自动部署
"""

import subprocess
import sys
import os

def run_command(cmd, cwd=None):
    """运行命令"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print(f"警告: {result.stderr}", file=sys.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return False

def main():
    print("=" * 60)
    print("开始每日简报更新流程")
    print("=" * 60)
    
    # 1. 抓取数据
    print("\n[1/3] 正在抓取数据...")
    if not run_command("python3 fetch_data.py", cwd="/workspace/每日简报-完整版"):
        print("❌ 数据抓取失败")
        return 1
    
    # 2. 生成 HTML
    print("\n[2/3] 正在生成 HTML...")
    if not run_command("python3 generate_html.py", cwd="/workspace/每日简报-完整版"):
        print("❌ HTML 生成失败")
        return 1
    
    # 3. 部署到 GitHub
    print("\n[3/3] 正在部署到 GitHub...")
    os.chdir("/workspace/每日简报-完整版")
    
    # 配置 git
    run_command('git config user.name "GitHub Action"')
    run_command('git config user.email "action@github.com"')
    
    # 提交和推送
    if run_command("git add ."):
        if run_command('git commit -m "每日简报自动更新"'):
            if run_command("git push origin main"):
                print("\n" + "=" * 60)
                print("✅ 已完成更新！")
                print("🌐 访问链接：https://jerry000020.github.io/daily-brief/")
                print("=" * 60)
                return 0
    
    print("\n⚠️  部署失败，请检查 git 配置")
    return 1

if __name__ == '__main__':
    sys.exit(main())
