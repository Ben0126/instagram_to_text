#!/usr/bin/env python3
"""
Instagram 文案抓取測試腳本
用於測試不同的 Instagram URL 並比較抓取結果
"""

import asyncio
import sys
from main import get_post_caption

# 測試用的 URL 列表
TEST_URLS = [
    "https://www.instagram.com/reel/DLbk7VgOwPV/",  # 您提供的 Reel
    # 您可以在這裡添加更多測試 URL
]

async def test_single_url(url: str) -> dict:
    """測試單個 URL"""
    print(f"\n{'='*60}")
    print(f"測試 URL: {url}")
    print('='*60)
    
    try:
        result = await get_post_caption(url)
        success = not result.startswith("ERROR:")
        
        return {
            "url": url,
            "success": success,
            "result": result,
            "length": len(result) if success else 0
        }
    except Exception as e:
        return {
            "url": url,
            "success": False,
            "result": f"Exception: {e}",
            "length": 0
        }

async def run_tests():
    """執行所有測試"""
    print("🚀 Instagram 文案抓取測試開始")
    print(f"總共 {len(TEST_URLS)} 個測試 URL")
    
    results = []
    
    for url in TEST_URLS:
        result = await test_single_url(url)
        results.append(result)
        
        # 顯示簡短摘要
        status = "✅ 成功" if result["success"] else "❌ 失敗"
        print(f"{status} - 長度: {result['length']} 字元")
        
        if result["success"]:
            # 顯示前 100 個字元的預覽
            preview = result["result"][:100] + "..." if len(result["result"]) > 100 else result["result"]
            print(f"預覽: {preview}")
    
    # 總結報告
    print(f"\n{'='*60}")
    print("📊 測試總結")
    print('='*60)
    
    successful = sum(1 for r in results if r["success"])
    total = len(results)
    success_rate = (successful / total * 100) if total > 0 else 0
    
    print(f"成功率: {successful}/{total} ({success_rate:.1f}%)")
    
    for result in results:
        status = "✅" if result["success"] else "❌"
        print(f"{status} {result['url']} ({result['length']} 字元)")
        
        if not result["success"]:
            print(f"   錯誤: {result['result']}")

def add_test_url(url: str):
    """添加新的測試 URL"""
    if url not in TEST_URLS:
        TEST_URLS.append(url)
        print(f"✅ 已添加測試 URL: {url}")
    else:
        print(f"⚠️  URL 已存在: {url}")

async def main():
    """主函數"""
    if len(sys.argv) > 1:
        # 如果提供了 URL 參數，添加到測試列表
        for url in sys.argv[1:]:
            if "instagram.com/" in url:
                add_test_url(url)
            else:
                print(f"❌ 無效的 Instagram URL: {url}")
    
    if not TEST_URLS:
        print("❌ 沒有可測試的 URL")
        print("使用方法:")
        print("  python test_extraction.py")
        print("  python test_extraction.py <instagram_url1> <instagram_url2> ...")
        return
    
    await run_tests()

if __name__ == "__main__":
    asyncio.run(main()) 