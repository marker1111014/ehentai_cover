# E-Hentai 漫畫第一頁下載機器人

這是一個 Telegram 機器人，用於自動下載 E-Hentai 或 ExHentai 漫畫的第一頁圖片。

## 功能特點

- 自動下載 E-Hentai 或 ExHentai 漫畫的第一頁圖片
- 支援自動將 ExHentai 的 URL 轉換為 E-Hentai 的 URL
- 使用隨機 User-Agent 和請求頭，避免被封鎖
- 詳細的日誌記錄，方便追蹤問題
- 自動清理臨時檔案

## 安裝步驟

1. 克隆專案：
```bash
git clone <repository-url>
cd <repository-directory>
```

2. 安裝依賴套件：
```bash
pip install -r requirements.txt
```

3. 設置環境變數：
   - 創建 `.env` 檔案
   - 添加你的 Telegram Bot Token：
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

## 部署

### Railway 部署

1. 準備以下檔案：
   - `ehentai_cover_downloader.py`
   - `requirements.txt`
   - `Procfile`
   - `runtime.txt`
   - `.gitignore`

2. 在 Railway 中：
   - 創建新專案
   - 選擇 "Deploy from GitHub repo"
   - 設置環境變數 `TELEGRAM_BOT_TOKEN`

## 使用方法

1. 在 Telegram 中啟動機器人：
   - 發送 `/start` 命令

2. 發送漫畫 URL：
   - 直接發送 E-Hentai 或 ExHentai 的漫畫頁面 URL
   - 機器人會自動下載並發送第一頁圖片

## 技術細節

- 使用 Python 3.11
- 使用 `python-telegram-bot` 處理 Telegram 機器人功能
- 使用 `requests` 和 `BeautifulSoup` 進行網頁爬取
- 使用 `fake-useragent` 生成隨機 User-Agent
- 使用 `python-dotenv` 管理環境變數

## 注意事項

- 請確保你的 Telegram Bot Token 安全，不要公開分享
- 建議使用代理或 VPN 以避免 IP 被封鎖
- 請遵守 E-Hentai 的使用條款和 robots.txt

## 貢獻

歡迎提交 Pull Request 或提出 Issue！

## 授權

MIT License 