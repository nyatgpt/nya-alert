import os
import json
import requests
import telegram

# 初始化 Telegram bot
bot = telegram.Bot(token=os.environ["telegram_bot_token"])

# 測試用訊息，確認 BOT 是否可以發訊息
bot.send_message(chat_id=os.environ["telegram_chat_id"], text="✅ 測試訊息：BOT 可以發送訊息囉！")

# 讀取商品清單
with open("products.json", "r") as f:
    products = json.load(f)

def send_telegram_message(message):
    bot.send_message(chat_id=os.environ["telegram_chat_id"], text=message)

def check_stock():
    for product in products:
        try:
            response = requests.get(product["url"])
            page_text = response.text.lower()

            if any(keyword in page_text for keyword in ["在庫確認中", "売り切れ", "sold out"]):
                message = f"❌【{product['name']}】目前缺貨"
            else:
                message = f"✅【{product['name']}】有庫存啦！\n🔗 {product['url']}"
            send_telegram_message(message)

        except Exception as e:
            send_telegram_message(f"⚠️ 檢查【{product['name']}】時發生錯誤：{str(e)}")

if __name__ == "__main__":
    check_stock()
