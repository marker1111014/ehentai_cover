import requests
from bs4 import BeautifulSoup
import os
import logging
from datetime import datetime
import re
from fake_useragent import UserAgent
import random
from urllib.parse import urlparse, urlunparse
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio
import tempfile
from dotenv import load_dotenv

# 載入 .env 檔案
load_dotenv()

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ehentai_download.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# 從環境變數讀取 Telegram Bot Token
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    logging.error("無法讀取 Telegram Bot Token，請檢查 .env 檔案")
    raise ValueError("請在 .env 檔案中設置 TELEGRAM_BOT_TOKEN")

def convert_to_ehentai(url):
    """將 exhentai.org 的 URL 轉換為 e-hentai.org"""
    parsed_url = urlparse(url)
    if parsed_url.netloc == 'exhentai.org':
        logging.info(f"檢測到 exhentai.org 網域，自動轉換為 e-hentai.org")
        # 替換網域
        new_netloc = 'e-hentai.org'
        # 重新組裝 URL
        converted_url = urlunparse((
            parsed_url.scheme,
            new_netloc,
            parsed_url.path,
            parsed_url.params,
            parsed_url.query,
            parsed_url.fragment
        ))
        logging.info(f"轉換後的 URL: {converted_url}")
        return converted_url
    return url

def get_random_headers():
    # 初始化 UserAgent
    ua = UserAgent()
    
    # 隨機選擇一個瀏覽器類型
    browser_type = random.choice(['chrome', 'firefox', 'safari', 'edge'])
    
    # 生成隨機的 User-Agent
    user_agent = getattr(ua, browser_type)
    
    # 隨機的 Accept-Language
    languages = ['zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                'en-US,en;q=0.9',
                'ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7',
                'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7']
    
    # 隨機的 Accept-Encoding
    encodings = ['gzip, deflate, br',
                'gzip, deflate',
                'br, gzip, deflate']
    
    # 隨機的 Accept
    accepts = ['text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8']
    
    headers = {
        'User-Agent': user_agent,
        'Accept': random.choice(accepts),
        'Accept-Language': random.choice(languages),
        'Accept-Encoding': random.choice(encodings),
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': random.choice(['max-age=0', 'no-cache', 'no-store']),
        'DNT': random.choice(['1', '0']),
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1'
    }
    
    # 隨機添加一些額外的請求頭
    if random.random() > 0.5:
        headers['Referer'] = 'https://www.google.com/'
    
    if random.random() > 0.5:
        headers['Pragma'] = 'no-cache'
    
    return headers

def extract_image_url(style_string):
    # 使用正則表達式從 style 屬性中提取圖片 URL
    match = re.search(r'url\((.*?)\)', style_string)
    if match:
        return match.group(1)
    return None

async def download_cover(gallery_url, update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        logging.info(f"收到下載請求，URL: {gallery_url}")
        # 檢查並轉換 URL
        gallery_url = convert_to_ehentai(gallery_url)
        
        # 獲取隨機請求頭
        headers = get_random_headers()
        logging.info(f"使用隨機 User-Agent: {headers['User-Agent']}")
        
        # 發送請求獲取頁面內容
        response = requests.get(gallery_url, headers=headers)
        logging.info(f"HTTP 狀態碼: {response.status_code}")
        
        # 檢查狀態碼
        if response.status_code != 200:
            error_msg = f"頁面訪問失敗，狀態碼: {response.status_code}"
            logging.error(error_msg)
            return None
            
        # 檢查內容長度
        content_length = len(response.text)
        logging.info(f"頁面內容長度: {content_length} 字節")
        
        if content_length == 0:
            error_msg = "頁面內容為空"
            logging.error(error_msg)
            return None
            
        # 使用 BeautifulSoup 解析頁面
        soup = BeautifulSoup(response.text, 'html.parser')
        logging.info("頁面解析成功")
        
        # 找到包含封面圖片的 div 元素
        cover_div = soup.find('div', style=lambda s: s and 'background:' in s and 'url(' in s)
        if not cover_div:
            error_msg = "找不到封面圖片元素"
            logging.error(error_msg)
            return None
            
        # 從 style 屬性中提取圖片 URL
        style = cover_div.get('style')
        img_url = extract_image_url(style)
        
        if not img_url:
            error_msg = "無法從 style 屬性中提取圖片 URL"
            logging.error(error_msg)
            return None
            
        logging.info(f"找到圖片 URL: {img_url}")
        
        # 獲取新的隨機請求頭用於下載圖片
        img_headers = get_random_headers()
        logging.info(f"使用新的隨機 User-Agent 下載圖片: {img_headers['User-Agent']}")
        
        # 下載圖片
        img_response = requests.get(img_url, headers=img_headers)
        logging.info(f"圖片下載狀態碼: {img_response.status_code}")
        
        if img_response.status_code != 200:
            error_msg = f"圖片下載失敗，狀態碼: {img_response.status_code}"
            logging.error(error_msg)
            return None
            
        # 檢查圖片內容長度
        img_content_length = len(img_response.content)
        logging.info(f"圖片大小: {img_content_length} 字節")
        
        if img_content_length == 0:
            error_msg = "圖片內容為空"
            logging.error(error_msg)
            return None
            
        # 生成唯一的檔案名稱
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'cover_{timestamp}.jpg'
        
        # 使用臨時檔案保存圖片
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_file.write(img_response.content)
            temp_file_path = temp_file.name
        
        return temp_file_path
        
    except requests.exceptions.RequestException as e:
        error_msg = f"請求發生錯誤: {str(e)}"
        logging.error(error_msg)
        logging.exception("詳細錯誤信息：")
        return None
    except Exception as e:
        error_msg = f"發生未知錯誤: {str(e)}"
        logging.error(error_msg)
        logging.exception("詳細錯誤信息：")
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理 /start 命令"""
    logging.info(f"收到 /start 命令，用戶 ID: {update.effective_user.id}")
    await update.message.reply_text(
        "歡迎使用 E-Hentai 封面下載機器人！\n"
        "請直接發送 E-Hentai 或 ExHentai 的漫畫頁面 URL，我會幫你下載封面圖片。"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理 /help 命令"""
    logging.info(f"收到 /help 命令，用戶 ID: {update.effective_user.id}")
    await update.message.reply_text(
        "使用說明：\n"
        "1. 直接發送 E-Hentai 或 ExHentai 的漫畫頁面 URL\n"
        "2. 我會自動下載並發送封面圖片給你\n"
        "3. 支援的網域：\n"
        "   - e-hentai.org\n"
        "   - exhentai.org（會自動轉換為 e-hentai.org）"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理用戶發送的訊息"""
    try:
        logging.info(f"收到訊息，用戶 ID: {update.effective_user.id}")
        logging.info(f"訊息內容: {update.message.text}")
        
        # 檢查訊息是否為 URL
        if not update.message.text.startswith(('http://', 'https://')):
            logging.warning("無效的 URL 格式")
            return
        
        # 檢查是否為支援的網域
        if 'e-hentai.org' not in update.message.text and 'exhentai.org' not in update.message.text:
            logging.warning(f"不支援的網域: {update.message.text}")
            return
        
        # 下載圖片
        image_path = await download_cover(update.message.text, update, context)
        
        if image_path:
            # 只發送圖片，不發送任何文字訊息
            await update.message.reply_photo(
                photo=open(image_path, 'rb'),
                reply_to_message_id=update.message.message_id
            )
            # 刪除臨時檔案
            os.unlink(image_path)
            logging.info("臨時檔案已刪除")
        else:
            logging.error("無法下載圖片")
    except Exception as e:
        logging.error(f"處理訊息時發生錯誤: {str(e)}", exc_info=True)

def main():
    """啟動機器人"""
    logging.info("Telegram 機器人開始執行")
    # 創建應用程式
    application = Application.builder().token(TOKEN).build()
    
    # 添加處理器
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # 啟動機器人
    logging.info("開始輪詢更新...")
    application.run_polling()

if __name__ == "__main__":
    logging.info("程式開始執行")
    main() 