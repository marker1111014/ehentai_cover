# E-Hentai 封面下載 Telegram 機器人

本專案是一個使用 Python 實現的 Telegram 機器人，能夠自動從 E-Hentai 或 ExHentai 漫畫頁面下載其第一頁圖片（即封面），並將圖片發送給發送連結的 Telegram 用戶。

## 功能特點

- **支持 e-hentai.org 及 exhentai.org 網域**（exhentai 的地址會自動轉為 e-hentai 處理）。
- 接收用戶發送的 E-Hentai/ExHentai 漫畫頁面 URL，自動解析並下載第一頁圖片。
- 圖片將作為回覆直接發送給用戶。
- 支持 `/start` 和 `/help` 指令，提供新手引導及使用說明。
- 針對請求頭採用隨機 UA 及其他參數，提升抓取穩定性。
- 具有詳細日誌紀錄，有助於除錯。

---

## 安裝與部署

### 前置需求

1. **Python 3.8+**
2. **Telegram Bot Token**  
   申請方式: [Telegram 官方 BotFather](https://core.telegram.org/bots#botfather)
3. **E-Hentai/ExHentai 可正常訪問權限**

### 依賴安裝

建議使用虛擬環境：

```bash
python -m venv venv
source venv/bin/activate  # Windows 用戶請執行 venv\Scripts\activate
```

安裝依賴：

```bash
pip install -r requirements.txt
```

**`requirements.txt` 內容建議如下：**

```
requests
beautifulsoup4
python-telegram-bot>=20.0
fake-useragent
python-dotenv
```

### 設定環境變數

新建 `.env` 檔案於專案根目錄，加入：

```
TELEGRAM_BOT_TOKEN=你的 Telegram Bot Token
```

---

## 使用說明

### 啟動機器人

```bash
python 你的主程式文件名.py
```

### 指令與使用流程

- `/start`
  - 顯示歡迎介紹。
- `/help`
  - 顯示詳細使用說明與支持的網域。
- **直接發送 E-Hentai 或 ExHentai 的漫畫頁面 URL**
  - 機器人自動回傳該漫畫的封面圖片（即第一頁圖片）。

### 使用場景示例

用戶直接發送：

```
https://e-hentai.org/g/xxxxxxx/xxxxxxxx/
```

機器人回復該漫畫的第一頁圖片。

---

## 主要程式邏輯說明

- **convert_to_ehentai(url)**  
  自動將 exhentai 的 url 轉成 e-hentai，保證後續流程順暢。
- **get_random_headers()**  
  隨機生成偽裝請求標頭（含 UA、語言等），防止被封。
- **download_cover(gallery_url, update, context)**  
  解析並下載漫畫的第一頁原圖，存儲為臨時文件。
- **extract_urls(text)**  
  使用正則從訊息中提取所有網址。
- **start/help/handle_message**  
  對應 /start、/help 指令，以及通用文字消息的自動回覆與處理。
- **main()**  
  主流程：加載 Token，註冊處理器，開始 long polling。

---

## 日誌

- 預設會將詳盡運行日誌輸出到檔案 `ehentai_download.log`，也會同時顯示於終端機。
- 各環節錯誤都有詳細記錄，有助於維護與擴展。

---

## 注意事項

- 本機器人僅應用於學術技術研究用途，請勿用於任何非法用途。
- 有些漫畫頁面可能因版權、網路環境或驗證問題無法直接存取或抓取，這屬於正常現象。
- 若遇圖片或頁面無法下載，請先確認本地網路及 e-hentai 是否可正常訪問。

---

## 貢獻與問題回報

如有建議、bug 回報或功能補完，歡迎提出 Issue 或 Pull Request。

---

## 授權

本專案開源，採用 MIT License。

---

> **本工具僅供個人學習研究，不對第三方資源或商標負任何法律責任。**

---

如果你要加入範例 `requirements.txt` 檔案內容，可將下段複製粘貼：

```
requests
beautifulsoup4
python-telegram-bot>=20.0
fake-useragent
python-dotenv
```

---
