import os
import json
import requests
import telegram

# 讀取 Telegram Token 和 Chat ID（大小寫需與 GitHub Secrets 相符）
bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
chat_id = os.environ["TELEGRAM_CHAT_ID"]

# 建立 Telegram Bot 物件
bot = telegram.Bot(token=bot_token)

# 🔧 測試訊息（你可移除這段）
bot.send_message(chat_id=chat_id, text="✅ 測試訊息：Bot 設定成功！")

# 發送訊息的函式
def send_telegram_message(message):
    bot.send_message(chat_id=chat_id, text=message)

# 檢查庫存的函式
def check_stock():
    with open("products.json", "r", encoding="utf-8") as f:
        products = json.load(f)

    for product in products:
        try:
            response = requests.get(product["url"])
            response.raise_for_status()  # 若網站有錯誤，會丟出 exception

            page_text = response.text.lower()

            # 根據常見「缺貨」關鍵字判斷
            if any(keyword in page_text for keyword in ["在庫確認中", "売り切れ", "sold out"]):
                print(f"{product['name']} 缺貨中")
            else:
                message = f"📦【{product['name']}】有庫存啦！\n🔗 {product['url']}"
                send_telegram_message(message)

        except Exception as e:
            print(f"❌ 檢查 {product['name']} 時發生錯誤：{e}")

# 主程序入口
if __name__ == "__main__":
    check_stock()
