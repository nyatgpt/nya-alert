import requests
import json
import telegram
import os

# 臨時測試用，確認訊息是否發得出去
bot = telegram.Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])
bot.send_message(chat_id=os.environ["TELEGRAM_CHAT_ID"], text="這是一則測試訊息 from GitHub Actions")

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
            response = requests.get(product["url"])

            # 假設商品頁面有「カートに追加する」字樣來檢查庫存狀態
            if "カートに追加する" in response.text:
                message = f"📦【{product['name']}】有庫存啦！\n🔗 {product['url']}"
            else:
                message = f"❌【{product['name']}】目前無庫存"
            
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
