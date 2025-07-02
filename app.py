from flask import Flask, render_template, request, jsonify, send_file
import asyncio
import json
import datetime
import os
import random
import time
from urllib.parse import urlparse
import threading
from concurrent.futures import ThreadPoolExecutor

# 智慧依賴檢查
def check_dependencies():
    """檢查並自動安裝缺失的依賴"""
    missing_deps = []
    
    try:
        from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
    except ImportError:
        missing_deps.append("playwright")
    
    try:
        import flask
    except ImportError:
        missing_deps.append("flask")
    
    if missing_deps:
        print("❌ 檢測到缺失的依賴套件:")
        for dep in missing_deps:
            print(f"   - {dep}")
        
        print("\n請執行以下指令安裝依賴:")
        print("pip install flask playwright")
        print("playwright install chromium")
        return False
    
    return True

# 檢查依賴
if not check_dependencies():
    exit(1)

from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

app = Flask(__name__)

# 反偵測策略配置
ANTI_DETECTION_CONFIG = {
    "user_agents": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59"
    ],
    "viewport_sizes": [
        {"width": 1920, "height": 1080},
        {"width": 1366, "height": 768},
        {"width": 1440, "height": 900},
        {"width": 1536, "height": 864}
    ],
    "delays": {
        "page_load": (2, 5),
        "between_actions": (1, 3),
        "between_requests": (3, 8)
    }
}

async def extract_caption_from_meta(page) -> tuple[str, str]:
    """從 meta 標籤中提取文案"""
    try:
        # 嘗試從 og:description meta 標籤獲取
        og_description = await page.get_attribute('meta[property="og:description"]', 'content')
        if og_description and len(og_description) > 50:
            match = re.search(r':\s*"([^"]+)"', og_description)
            if match:
                return match.group(1).strip(), "meta_og_description"
            cleaned = re.sub(r'^[^:]+:\s*', '', og_description)
            return cleaned.strip(), "meta_og_description"
        
        # 嘗試從 description meta 標籤獲取
        description = await page.get_attribute('meta[name="description"]', 'content')
        if description and len(description) > 50:
            match = re.search(r':\s*"([^"]+)"', description)
            if match:
                return match.group(1).strip(), "meta_description"
            cleaned = re.sub(r'^[^:]+:\s*', '', description)
            return cleaned.strip(), "meta_description"
            
    except Exception as e:
        print(f"Meta 標籤抓取失敗: {e}")
    
    return "", "failed"

async def get_single_post_caption(url: str, browser_context=None) -> dict:
    """抓取單個Instagram貼文的文案，包含反偵測策略"""
    result = {
        "url": url,
        "timestamp": datetime.datetime.now().isoformat(),
        "caption": "",
        "success": False,
        "method": "",
        "length": 0,
        "error": None
    }
    
    try:
        # 反偵測策略：隨機選擇配置
        user_agent = random.choice(ANTI_DETECTION_CONFIG["user_agents"])
        viewport = random.choice(ANTI_DETECTION_CONFIG["viewport_sizes"])
        
        # 如果沒有提供browser context，創建新的
        if browser_context is None:
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-blink-features=AutomationControlled']
                )
                context = await browser.new_context(
                    user_agent=user_agent,
                    viewport=viewport
                )
                page = await context.new_page()
                try:
                    result = await _extract_caption_from_page(page, url, result)
                finally:
                    await context.close()
                    await browser.close()
        else:
            page = await browser_context.new_page()
            try:
                result = await _extract_caption_from_page(page, url, result)
            finally:
                await page.close()
                
    except Exception as e:
        result["error"] = f"未預期的錯誤: {str(e)}"
    
    return result

async def _extract_caption_from_page(page, url: str, result: dict) -> dict:
    """從頁面提取文案的核心邏輯"""
    try:
        # 反偵測策略：添加隨機延遲
        await asyncio.sleep(random.uniform(*ANTI_DETECTION_CONFIG["delays"]["page_load"]))
        
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(random.uniform(*ANTI_DETECTION_CONFIG["delays"]["page_load"]))

        # 關閉彈窗
        await page.keyboard.press('Escape')
        await asyncio.sleep(random.uniform(*ANTI_DETECTION_CONFIG["delays"]["between_actions"]))

        caption = ""
        method = ""
        
        # 嘗試從頁面元素抓取文案
        caption_selectors = [
            'article div[data-testid="post-shared-text"] span',
            'article span[dir="auto"]',
            'div[data-testid="post-shared-text"]',
            'span[dir="auto"]',
            'div[role="button"] span',
        ]
        
        for selector in caption_selectors:
            try:
                elements = page.locator(selector)
                count = await elements.count()
                
                if count > 0:
                    for i in range(min(count, 10)):  # 限制檢查數量
                        try:
                            text = await elements.nth(i).inner_text()
                            text = text.strip()
                            
                            if (len(text) > 20 and 
                                "很抱歉" not in text and 
                                "播放此影片時發生問題" not in text and
                                "Instagram" not in text and
                                "登入" not in text):
                                
                                if len(text) > len(caption):
                                    caption = text
                                    method = f"page_element_{selector}"
                        except:
                            continue
                            
            except:
                continue
        
        # 如果頁面抓取結果不理想，嘗試meta標籤
        if not caption or len(caption) < 30:
            meta_caption, meta_method = await extract_caption_from_meta(page)
            if meta_caption and len(meta_caption) > len(caption):
                caption = meta_caption
                method = meta_method
        
        if caption and len(caption) > 10:
            result["caption"] = caption
            result["success"] = True
            result["method"] = method
            result["length"] = len(caption)
        else:
            result["error"] = "無法找到文案內容"
            
    except PlaywrightTimeoutError:
        result["error"] = "頁面載入超時"
    except Exception as e:
        result["error"] = f"抓取過程錯誤: {str(e)}"
    
    return result

async def batch_extract_captions(urls: list) -> list:
    """批量抓取Instagram文案，使用反偵測策略"""
    results = []
    
    # 限制最多5個URL
    urls = urls[:5]
    
    async with async_playwright() as p:
        # 反偵測策略：使用隨機配置
        user_agent = random.choice(ANTI_DETECTION_CONFIG["user_agents"])
        viewport = random.choice(ANTI_DETECTION_CONFIG["viewport_sizes"])
        
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox', 
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ]
        )
        
        context = await browser.new_context(
            user_agent=user_agent,
            viewport=viewport
        )
        
        try:
            for i, url in enumerate(urls):
                if i > 0:
                    # 反偵測策略：請求間隨機延遲
                    delay = random.uniform(*ANTI_DETECTION_CONFIG["delays"]["between_requests"])
                    print(f"等待 {delay:.1f} 秒後處理下一個URL...")
                    await asyncio.sleep(delay)
                
                print(f"處理第 {i+1}/{len(urls)} 個URL: {url}")
                result = await get_single_post_caption(url, context)
                results.append(result)
                
        finally:
            await context.close()
            await browser.close()
    
    return results

def save_batch_results_to_json(results: list, output_dir: str = "output") -> str:
    """保存批量抓取結果為JSON文件"""
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"instagram_batch_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)
    
    batch_data = {
        "batch_info": {
            "timestamp": datetime.datetime.now().isoformat(),
            "total_urls": len(results),
            "successful": sum(1 for r in results if r["success"]),
            "failed": sum(1 for r in results if not r["success"])
        },
        "results": results
    }
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(batch_data, f, ensure_ascii=False, indent=2)
    
    return filepath

def validate_instagram_url(url: str) -> bool:
    """驗證Instagram URL格式"""
    try:
        parsed = urlparse(url)
        return (parsed.netloc in ['www.instagram.com', 'instagram.com'] and 
                ('/p/' in parsed.path or '/reel/' in parsed.path))
    except:
        return False

@app.route('/')
def index():
    """主頁面"""
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract_captions():
    """處理文案抓取請求"""
    try:
        data = request.get_json()
        urls_text = data.get('urls', '').strip()
        
        if not urls_text:
            return jsonify({"error": "請提供Instagram URL"}), 400
        
        # 解析URL列表
        urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
        
        # 驗證URL格式
        valid_urls = []
        invalid_urls = []
        
        for url in urls:
            if validate_instagram_url(url):
                valid_urls.append(url)
            else:
                invalid_urls.append(url)
        
        if not valid_urls:
            return jsonify({"error": "沒有有效的Instagram URL"}), 400
        
        if len(valid_urls) > 5:
            return jsonify({"error": "最多只能處理5個URL"}), 400
        
        # 執行批量抓取
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            results = loop.run_until_complete(batch_extract_captions(valid_urls))
        finally:
            loop.close()
        
        # 保存結果
        json_filepath = save_batch_results_to_json(results)
        
        # 準備回應
        response_data = {
            "success": True,
            "total_processed": len(results),
            "successful": sum(1 for r in results if r["success"]),
            "failed": sum(1 for r in results if not r["success"]),
            "invalid_urls": invalid_urls,
            "results": results,
            "json_file": json_filepath
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({"error": f"處理錯誤: {str(e)}"}), 500

@app.route('/health')
def health_check():
    """健康檢查"""
    return jsonify({"status": "ok", "timestamp": datetime.datetime.now().isoformat()})

@app.route('/output/<filename>')
def download_file(filename):
    """下載輸出文件"""
    try:
        return send_file(
            os.path.join('output', filename),
            as_attachment=True,
            download_name=filename,
            mimetype='application/json'
        )
    except FileNotFoundError:
        return jsonify({"error": "文件不存在"}), 404

if __name__ == '__main__':
    # 確保模板目錄存在
    os.makedirs('templates', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    
    print("🚀 Instagram 文案抓取器 Web 版本")
    print("📝 支持批量抓取（最多5筆）")
    print("🛡️ 內建反偵測策略")
    print("🌐 啟動中...")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 