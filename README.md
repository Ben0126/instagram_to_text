# Instagram 文案抓取器

一個強大且穩定的 Instagram 貼文和 Reels 文案抓取工具，支援多種抓取策略以提高成功率。

## 功能特色

- ✅ **多重抓取策略**: 結合頁面元素和 meta 標籤抓取
- ✅ **支援繁體中文**: 完整的中文介面和錯誤訊息
- ✅ **自動展開功能**: 自動點擊 "更多" 按鈕展開完整文案
- ✅ **智慧選擇器**: 使用多種 CSS 選擇器提高抓取成功率
- ✅ **錯誤處理**: 完整的錯誤處理和 debug 檔案生成
- ✅ **支援多種格式**: 同時支援貼文 (Posts) 和短影片 (Reels)

## 快速開始

### 1. 安裝依賴

```bash
# 安裝 Python 套件
pip install -r requirements.txt

# 安裝 Playwright 瀏覽器
playwright install chromium
```

### 2. 基本使用

```bash
# 抓取單個 Instagram 貼文
python main.py https://www.instagram.com/p/YOUR_POST_ID/

# 抓取 Instagram Reel
python main.py https://www.instagram.com/reel/YOUR_REEL_ID/
```

### 3. 測試功能

```bash
# 執行預設測試
python test_extraction.py

# 測試特定 URL
python test_extraction.py https://www.instagram.com/reel/DLbk7VgOwPV/

# 測試多個 URL
python test_extraction.py <url1> <url2> <url3>
```

## 工作原理

### 多重抓取策略

1. **頁面元素抓取** (主要方法)
   - 自動展開 "更多" 按鈕
   - 使用多種 CSS 選擇器
   - 選擇最長且有意義的文字內容

2. **Meta 標籤抓取** (備用方法)
   - 從 `og:description` 抓取
   - 從 `description` meta 標籤抓取
   - 自動清理格式

3. **錯誤處理**
   - 自動生成 debug 截圖
   - 保存完整的 HTML 內容
   - 詳細的錯誤訊息

### 支援的選擇器

```python
caption_selectors = [
    'div[data-testid="post-shared-text"]',  # 主要的文案容器
    'h1',                                    # 標題元素
    'article span[dir="auto"]',              # 文章內的文字
    'div[role="button"] span',               # 按鈕內的文字
    'span._ap3a._aaco._aacu._aacx._aada',    # Instagram 特定 class
    'div[data-testid="post-shared-text"] span',  # 文案容器內的 span
    'meta + div span[dir="auto"]'            # meta 標籤後的文字
]
```

## 檔案說明

- `main.py` - 主要的抓取程式
- `test_extraction.py` - 測試腳本
- `requirements.txt` - Python 依賴需求
- `debug_page.html` - 抓取失敗時生成的 HTML 檔案
- `debug_screenshot.png` - 抓取失敗時生成的截圖

## 常見問題

### Q: 程式運行時會開啟瀏覽器視窗嗎？
A: 是的，目前設定為 `headless=False` 以便觀察抓取過程。如需無頭模式，請修改 `main.py` 中的 `launch(headless=True)`。

### Q: 如果抓取失敗怎麼辦？
A: 程式會自動生成 `debug_page.html` 和 `debug_screenshot.png` 檔案，您可以查看這些檔案來診斷問題。

### Q: 支援哪些 Instagram URL 格式？
A: 支援標準的 Instagram URL 格式：
- `https://www.instagram.com/p/POST_ID/`
- `https://www.instagram.com/reel/REEL_ID/`
- 包含參數的 URL 也可以正常處理

### Q: 如何提高抓取成功率？
A: 確保網路連線穩定，Instagram 頁面能正常載入。如果持續失敗，可以檢查 debug 檔案找出問題。

## 技術細節

- **瀏覽器**: Chromium (透過 Playwright)
- **語言**: Python 3.7+
- **編碼**: UTF-8 支援完整中文處理
- **超時設定**: 頁面載入 60 秒，元素等待 15 秒
- **錯誤重試**: 多選擇器自動重試機制

## 開發計劃

- [ ] 新增批次處理功能
- [ ] 支援更多社交媒體平台
- [ ] 新增 GUI 介面
- [ ] 新增文案情感分析功能
- [ ] 新增匯出功能 (CSV, JSON)

## 貢獻

歡迎提交 Issue 和 Pull Request 來改進這個專案！

## 授權

MIT License 