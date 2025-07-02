#!/usr/bin/env python3
"""
Instagram 文案抓取器快速設定腳本
自動安裝依賴並進行環境檢查
"""

import sys
import subprocess
import os
import asyncio

def run_command(command):
    """執行系統指令"""
    try:
        print(f"執行: {command}")
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ 成功: {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 失敗: {command}")
        print(f"錯誤: {e.stderr}")
        return False

def check_python_version():
    """檢查 Python 版本"""
    version = sys.version_info
    print(f"Python 版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 7:
        print("✅ Python 版本符合需求 (3.7+)")
        return True
    else:
        print("❌ Python 版本不符合需求，需要 3.7 或更高版本")
        return False

def install_requirements():
    """安裝 Python 套件需求"""
    print("\n📦 安裝 Python 套件...")
    
    # 先升級 pip
    if not run_command(f"{sys.executable} -m pip install --upgrade pip"):
        return False
    
    # 安裝需求套件
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt"):
        return False
    
    return True

def install_playwright():
    """安裝 Playwright 瀏覽器"""
    print("\n🌐 安裝 Playwright 瀏覽器...")
    
    if not run_command(f"{sys.executable} -m playwright install chromium"):
        return False
    
    return True

def test_installation():
    """測試安裝是否成功"""
    print("\n🧪 測試安裝...")
    
    try:
        # 測試導入必要模組
        import playwright
        print("✅ Playwright 導入成功")
        
        from playwright.async_api import async_playwright
        print("✅ Playwright API 導入成功")
        
        # 測試 main.py 是否可以導入
        if os.path.exists('main.py'):
            import main
            print("✅ main.py 導入成功")
        
        return True
        
    except ImportError as e:
        print(f"❌ 導入測試失敗: {e}")
        return False

async def quick_test():
    """快速功能測試"""
    print("\n🚀 執行快速功能測試...")
    
    try:
        from main import extract_caption_from_meta
        from playwright.async_api import async_playwright
        
        # 簡單的瀏覽器啟動測試
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto("https://example.com")
            await browser.close()
        
        print("✅ 瀏覽器啟動測試成功")
        return True
        
    except Exception as e:
        print(f"❌ 功能測試失敗: {e}")
        return False

def main():
    """主安裝流程"""
    print("🎯 Instagram 文案抓取器 - 快速設定")
    print("=" * 50)
    
    success = True
    
    # 1. 檢查 Python 版本
    if not check_python_version():
        success = False
        print("\n❌ 請升級 Python 到 3.7 或更高版本")
        return
    
    # 2. 安裝 Python 套件
    if not install_requirements():
        success = False
        print("\n❌ Python 套件安裝失敗")
        return
    
    # 3. 安裝 Playwright 瀏覽器
    if not install_playwright():
        success = False
        print("\n❌ Playwright 瀏覽器安裝失敗")
        return
    
    # 4. 測試安裝
    if not test_installation():
        success = False
        print("\n❌ 安裝測試失敗")
        return
    
    # 5. 快速功能測試
    try:
        asyncio.run(quick_test())
    except Exception as e:
        print(f"⚠️  功能測試跳過: {e}")
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 安裝完成！")
        print("=" * 50)
        print("\n📖 使用方法:")
        print("   python main.py <instagram_url>")
        print("   python test_extraction.py")
        print("\n📋 範例:")
        print("   python main.py https://www.instagram.com/reel/DLbk7VgOwPV/")
        print("\n📚 更多資訊請查看 README.md")
    else:
        print("\n❌ 安裝過程中出現錯誤，請檢查上方訊息")

if __name__ == "__main__":
    main() 