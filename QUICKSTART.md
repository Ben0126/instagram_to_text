# 🚀 快速開始指南

## 📱 使用Web UI（推薦）

### 1. 安裝依賴
```bash
pip install flask
```

### 2. 啟動Web服務器
```bash
python app.py
```

### 3. 打開瀏覽器
在瀏覽器中訪問：**http://localhost:5000**

### 4. 使用界面
1. 📝 在文字框中貼上Instagram URL（每行一個，最多5個）
2. 🚀 點擊「開始抓取文案」按鈕
3. ⏳ 等待處理完成（約1-5分鐘）
4. 📊 查看抓取結果和統計
5. 📥 下載JSON格式的結果文件

---

## 💻 使用命令行（進階）

### 單個URL
```bash
python main.py https://www.instagram.com/reel/XXXXXXXXX/
```

### 查看結果
結果會自動保存在 `output/` 目錄中的JSON文件

---

## ✨ 主要功能

- 🎯 **支援格式**：Instagram貼文 (/p/) 和 Reels (/reel/)
- 🔄 **批量處理**：一次最多5個URL
- 🛡️ **反偵測**：內建多重反偵測策略
- 📄 **JSON輸出**：結構化數據格式
- 🌐 **Web界面**：無需命令行操作

## 🆘 需要幫助？

查看完整說明文檔：[README_WEB.md](README_WEB.md)

---

**🎉 就是這麼簡單！馬上開始抓取Instagram文案吧！** 