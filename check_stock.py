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
    for product in products:
        response = requests.get(product["url"])

        # 假設商品頁面有「カートに追加する」字樣來檢查庫存狀態
        if "カートに追加する" in response.text:
            message = f"📦【{product['name']}】有庫存啦！\n🔗 {product['url']}"
        else:
            message = f"❌【{product['name']}】目前無庫存"
        
        send_telegram_message(message)

        except Exception as e:
            print(f"❌ 檢查 {product['name']} 時發生錯誤：{e}")

# 主程序入口
if __name__ == "__main__":
    check_stock()
