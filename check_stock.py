import telegram
import os

# 臨時測試用，確認訊息是否發得出去
bot = telegram.Bot(token=os.environ["telegram_bot_token"])
bot.send_message(chat_id=os.environ["telegram_chat_id"], text="這是一則測試訊息 from GitHub Actions")

# 設定 Telegram Bot Token 和 Chat ID
bot_token = "telegram_bot_token"  # 用你的 bot token 替換
chat_id = "telegram_chat_id"  # 用你的 chat_id 替換

# Telegram Bot 的 URL
url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

# 讀取商品資料
with open("products.json", "r") as f:
    products = json.load(f)

def check_stock():
    for product in products:
        # 假設商品頁面有「缺貨」字樣來檢查庫存狀態
        response = requests.get(product["url"])
        if "在庫確認中" in response.text.lower() or "売り切れ" in response.text.lower() or "SOLD OUT" in response.text.lower():  # 根據網頁內容檢查是否缺貨
            message = f"{product['name']} is out of stock."
        else:
            message = f"{product['name']} is in stock."

        # 發送 Telegram 訊息
def send_telegram_message(message):
    bot = telegram.Bot(token=os.environ["telegram_bot_token"])
    bot.send_message(chat_id=os.environ["telegram_chat_id"], text=message)

# ...
if in_stock:
    message = f"📦【{product['name']}】有庫存啦！\n🔗 {product['url']}"
    send_telegram_message(message)

if __name__ == "__main__":
    check_stock()
