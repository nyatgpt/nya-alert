import requests
import json
import telegram
import os

# 設定 Telegram Bot Token 和 Chat ID
bot_token = os.environ["TELEGRAM_BOT_TOKEN"]  # 用你的 bot token 替換
chat_id = os.environ["TELEGRAM_CHAT_ID"]  # 用你的 chat_id 替換

# Telegram Bot 的 URL
url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

# 讀取商品資料
with open("products.json", "r") as f:
    products = json.load(f)

def check_stock():
    for product in products:
        try:
            # 發送請求抓取商品頁面
            response = requests.get(product["url"])
            
            # 檢查頁面中是否存在庫存標記
            if "http://schema.org/InStock" in response.text:
                message = f"📦【{product['name']}】有庫存啦！\n🔗 {product['url']}"
                send_telegram_message(message)  # 只有有庫存時發送通知
            elif "http://schema.org/OutOfStock" in response.text:
                # 無庫存時不做任何處理，不發送通知
                pass
            else:
                # 如果無法確定庫存狀態，可以選擇發送「庫存狀態未知」通知
                message = f"⚠️【{product['name']}】庫存狀態未知\n🔗 {product['url']}"
                send_telegram_message(message)

        except Exception as e:
            # 捕捉異常並記錄錯誤
            error_message = f"Error checking {product['name']}: {e}"
            send_telegram_message(error_message)

def send_telegram_message(message):
    bot = telegram.Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])
    bot.send_message(chat_id=os.environ["TELEGRAM_CHAT_ID"], text=message)

if __name__ == "__main__":
    check_stock()
