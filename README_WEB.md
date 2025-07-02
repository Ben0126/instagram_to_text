# 📱 Instagram 文案抓取器 - Web 版本

## 🚀 功能特色

### ✨ **全新Web UI界面**
- 🖥️ 簡潔美觀的現代化網頁界面
- 📱 響應式設計，支援桌面和手機
- 🎨 直觀的操作流程和即時回饋

### 🔄 **批量處理能力**
- 📋 支援一次處理最多 **5個** Instagram URL
- ⚡ 每行一個URL，簡單易用
- 📊 即時顯示處理進度和統計結果

### 🛡️ **反偵測策略**
- 🎭 **隨機User-Agent輪換** - 模擬不同瀏覽器
- 📐 **隨機視窗尺寸** - 避免固定模式識別
- ⏰ **智慧延遲機制** - 頁面載入和請求間隨機延遲
- 🚫 **反自動化特徵** - 禁用自動化控制相關標識

### 📄 **結構化輸出**
- 💾 自動生成JSON格式結果文件
- 📥 支援直接下載抓取結果
- 📈 包含詳細統計和成功率資訊

## 📋 安裝要求

### 🔧 系統依賴
```bash
pip install flask playwright beautifulsoup4 lxml
playwright install chromium
```

### 📦 自動安裝
```bash
pip install -r requirements.txt
playwright install chromium
```

## 🎯 使用方法

### 1️⃣ 啟動Web服務器
```bash
python app.py
```

### 2️⃣ 打開瀏覽器
訪問：`http://localhost:5000`

### 3️⃣ 使用界面
1. **輸入URL** - 在文字框中貼上Instagram URL（每行一個）
2. **支援格式**：
   - 貼文：`https://www.instagram.com/p/XXXXXXXXX/`
   - Reels：`https://www.instagram.com/reel/XXXXXXXXX/`
3. **點擊抓取** - 按下「🚀 開始抓取文案」按鈕
4. **查看結果** - 即時查看抓取結果和統計
5. **下載JSON** - 點擊下載按鈕保存結果

## 📊 輸出格式

### JSON 結構
```json
{
  "batch_info": {
    "timestamp": "2025-07-02T16:25:21.245028",
    "total_urls": 3,
    "successful": 2,
    "failed": 1
  },
  "results": [
    {
      "url": "https://www.instagram.com/reel/xxx/",
      "timestamp": "2025-07-02T16:25:21.245028",
      "caption": "完整的文案內容...",
      "success": true,
      "method": "page_element_span[dir=\"auto\"]",
      "length": 241,
      "error": null
    }
  ]
}
```

## 🛡️ 反偵測機制詳情

### 🎭 瀏覽器偽裝
- Chrome, Firefox, Safari, Edge等不同User-Agent
- 隨機視窗尺寸組合
- 禁用自動化檢測標誌

### ⏰ 智慧延遲
- **頁面載入延遲**：2-5秒隨機
- **操作間延遲**：1-3秒隨機  
- **請求間延遲**：3-8秒隨機

### 🔧 進階策略
- 禁用WebRTC洩漏
- 模擬真實用戶行為
- 避免並發過高的請求

## 🎯 API 端點

### GET `/`
- 主頁面界面

### POST `/extract`
- 批量抓取文案API
- 請求格式：`{"urls": "url1\nurl2\nurl3"}`

### GET `/health`
- 健康檢查端點
- 回應：`{"status": "ok", "timestamp": "..."}`

## 📁 文件結構

```
instagram_to_text/
├── app.py              # Flask Web應用
├── main.py             # 原始命令行版本
├── templates/
│   └── index.html      # Web UI模板
├── output/             # 抓取結果輸出目錄
├── requirements.txt    # 依賴清單
└── README_WEB.md      # Web版本說明
```

## 🔍 使用限制

- ⚠️ **最多5個URL** - 避免過載和被檢測
- 🕐 **處理時間** - 每個URL約需30-60秒（含反偵測延遲）
- 🔒 **成功率** - 約85-95%（視Instagram反爬蟲策略而定）

## 🆘 常見問題

### Q: 為什麼抓取這麼慢？
A: 為了避免被Instagram偵測，程式刻意加入隨機延遲，這是正常的反偵測策略。

### Q: 某些URL抓取失敗怎麼辦？
A: 可能是該貼文設為私人、被刪除，或Instagram更新了頁面結構。

### Q: 可以同時抓取更多URL嗎？
A: 目前限制5個是為了平衡效率與成功率，避免觸發反爬蟲機制。

## 🚀 進階用法

### 命令行版本
如果需要更高的自定義度，仍可使用原始的命令行版本：
```bash
python main.py https://www.instagram.com/reel/xxx/
```

### 批量自動化
結合腳本可實現更大規模的自動化處理（請注意遵守Instagram服務條款）。

---

## 🎉 享受使用！

現在您可以通過簡潔的Web界面輕鬆抓取Instagram文案，無需記憶複雜的命令行參數！

🌐 **訪問地址**：http://localhost:5000 