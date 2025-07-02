import asyncio
import sys
import re

# 智慧依賴檢查
def check_dependencies():
    """檢查並自動安裝缺失的依賴"""
    missing_deps = []
    
    try:
        from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
    except ImportError:
        missing_deps.append("playwright")
    
    if missing_deps:
        print("❌ 檢測到缺失的依賴套件:")
        for dep in missing_deps:
            print(f"   - {dep}")
        
        print("\n🚀 請執行以下指令安裝依賴:")
        print("   python setup.py")
        print("   或手動安裝:")
        print("   pip install -r requirements.txt")
        print("   playwright install chromium")
        
        response = input("\n是否現在自動安裝? (y/N): ").lower().strip()
        if response in ['y', 'yes', '是']:
            import subprocess
            try:
                print("📦 正在安裝依賴...")
                subprocess.run([sys.executable, "setup.py"], check=True)
                print("✅ 依賴安裝完成，請重新運行程式")
            except subprocess.CalledProcessError:
                print("❌ 自動安裝失敗，請手動執行 python setup.py")
            except FileNotFoundError:
                print("❌ 未找到 setup.py，請手動安裝依賴")
        
        sys.exit(1)

# 執行依賴檢查
check_dependencies()

# 現在可以安全導入
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

async def extract_caption_from_meta(page) -> str:
    """
    從 meta 標籤中提取文案 - 優化版本
    """
    try:
        # 嘗試從 og:description meta 標籤獲取
        og_description = await page.get_attribute('meta[property="og:description"]', 'content')
        if og_description and len(og_description) > 50:
            print(f"從 og:description 抓取到文案 (長度: {len(og_description)})")
            # 清理格式，提取引號內的內容
            # 匹配模式：用戶名 於 日期 : "文案內容"
            match = re.search(r':\s*"([^"]+)"', og_description)
            if match:
                return match.group(1).strip()
            # 如果沒有引號格式，嘗試其他清理方式
            cleaned = re.sub(r'^[^:]+:\s*', '', og_description)
            return cleaned.strip()
        
        # 嘗試從 description meta 標籤獲取
        description = await page.get_attribute('meta[name="description"]', 'content')
        if description and len(description) > 50:
            print(f"從 description 抓取到文案 (長度: {len(description)})")
            # 清理格式，提取引號內的內容
            match = re.search(r':\s*"([^"]+)"', description)
            if match:
                return match.group(1).strip()
            # 如果沒有引號格式，嘗試其他清理方式
            cleaned = re.sub(r'^[^:]+:\s*', '', description)
            return cleaned.strip()
            
    except Exception as e:
        print(f"Meta 標籤抓取失敗: {e}")
    
    return ""

async def get_post_caption(url: str) -> str:
    """
    抓取Instagram貼文或Reels的文案，專注於右側文字內容
    """
    print("Launching browser in incognito mode...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        try:
            print(f"Navigating to {url}...")
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            await page.wait_for_timeout(3000)

            print("Attempting to close any popups by pressing Escape key...")
            await page.keyboard.press('Escape')
            print("Escape key pressed. Waiting for UI to settle...")
            await page.wait_for_timeout(2000)

            # --- 優化的抓取策略 ---
            caption = ""
            
            # 策略 1: 優先從頁面元素抓取文案 (不需要點擊更多按鈕)
            try:
                print("嘗試從頁面元素抓取文案...")
                
                # 優化的文案選擇器，針對Instagram右側文案區域
                caption_selectors = [
                    # Instagram 文案區域的常見選擇器
                    'article div[data-testid="post-shared-text"] span',
                    'article span[dir="auto"]',
                    'div[data-testid="post-shared-text"]',
                    'meta + div span[dir="auto"]',
                    # 通用的文案選擇器
                    'h1',
                    'span._ap3a._aaco._aacu._aacx._aada',
                    'span[dir="auto"]',
                    # 針對新版Instagram介面
                    'div[role="button"] span',
                    'article div span'
                ]
                
                for selector in caption_selectors:
                    try:
                        print(f"嘗試選擇器: {selector}")
                        elements = page.locator(selector)
                        count = await elements.count()
                        print(f"找到 {count} 個元素")
                        
                        if count > 0:
                            # 嘗試獲取最有意義的文字內容
                            for i in range(count):
                                try:
                                    text = await elements.nth(i).inner_text()
                                    text = text.strip()
                                    
                                    # 過濾掉明顯的錯誤訊息和短文字
                                    if (len(text) > 20 and 
                                        "很抱歉" not in text and 
                                        "播放此影片時發生問題" not in text and
                                        "Instagram" not in text and
                                        "登入" not in text):
                                        
                                        # 選擇最長且有意義的文字
                                        if len(text) > len(caption):
                                            caption = text
                                            print(f"找到更好的文案 (長度: {len(text)}): {text[:100]}...")
                                except Exception as e:
                                    continue
                                    
                    except Exception as e:
                        print(f"選擇器 {selector} 失敗: {e}")
                        continue
                
            except Exception as e:
                print(f"頁面元素抓取失敗: {e}")
            
            # 策略 2: 如果頁面抓取失敗或抓到的內容太短，從 meta 標籤抓取
            if not caption or len(caption) < 30:
                print("頁面元素抓取結果不理想，嘗試從 meta 標籤抓取...")
                meta_caption = await extract_caption_from_meta(page)
                if meta_caption and len(meta_caption) > len(caption):
                    caption = meta_caption
                    print(f"從 meta 標籤成功抓取文案 (長度: {len(caption)})")
            
            if caption and len(caption) > 10:
                return caption
            else:
                # 最後的 debug 處理
                print("所有策略都失敗，保存 debug 檔案...")
                await page.screenshot(path="debug_screenshot.png")
                with open("debug_page.html", "w", encoding="utf-8") as f:
                    f.write(await page.content())
                print("Debug 檔案已保存")
                return "ERROR: 無法找到文案內容。請檢查 debug 檔案。"

        except PlaywrightTimeoutError:
            print("ERROR: 頁面載入或處理超時")
            await page.screenshot(path="debug_screenshot.png")
            with open("debug_page.html", "w", encoding="utf-8") as f:
                f.write(await page.content())
            return "ERROR: 頁面處理超時。請檢查 debug 檔案。"
        except Exception as e:
            print(f"發生未預期的錯誤: {e}")
            return f"ERROR: 發生未預期的錯誤: {e}"
        finally:
            print("Closing browser...")
            await context.close()
            await browser.close()
            print("Browser closed.")

async def main():
    """
    Main function to run the scraper.
    Takes the Instagram URL as a command-line argument.
    """
    if len(sys.argv) < 2:
        print("--- Instagram 文案抓取器 ---")
        print("使用方法: python main.py <instagram_post_url>")
        print("範例: python main.py https://www.instagram.com/p/C2x5J8zR9A9/")
        print("     python main.py https://www.instagram.com/reel/DLbk7VgOwPV/")
        print("\n💡 提示: 如果是第一次使用，請先執行 python setup.py 安裝依賴")
        return

    post_url = sys.argv[1]

    if "instagram.com/" not in post_url:
        print("錯誤: 請提供有效的 Instagram URL。")
        return

    print(f"開始抓取: {post_url}")
    caption_text = await get_post_caption(post_url)

    print("\n" + "="*50)
    print("抓取到的文案:")
    print("="*50)
    print(caption_text)
    print("="*50 + "\n")

if __name__ == "__main__":
    asyncio.run(main())