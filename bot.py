import telebot
from telebot import types
import os
import json

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "6877877555"))

if not TOKEN:
    raise Exception("TOKEN topilmadi")

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(msg):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    web_app = types.WebAppInfo("https://gratofood.github.io/miniapp/")

    btn = types.KeyboardButton(
        text="🛍 Buyurtma berish",
        web_app=web_app
    )

    markup.add(btn)

    bot.send_message(
        msg.chat.id,
        "Buyurtma berish uchun tugmani bosing 👇",
        reply_markup=markup
    )


@bot.message_handler(content_types=["web_app_data"])
def webapp(msg):
    chat_id = msg.chat.id

    raw_data = msg.web_app_data.data
    print("RAW DATA:", raw_data)  # DEBUG

    try:
        data = json.loads(raw_data)
    except Exception as e:
        print("JSON ERROR:", e)
        bot.send_message(chat_id, "Xatolik ❌ (data noto‘g‘ri formatda)")
        return

    if not isinstance(data, list) or len(data) == 0:
        bot.send_message(chat_id, "Savat bo'sh ❌")
        return

    text = "🛒 Yangi zakaz:\n\n"

    counts = {}
    for item in data:
        counts[item] = counts.get(item, 0) + 1

    for item, qty in counts.items():
        text += f"{item} x{qty}\n"

    bot.send_message(ADMIN_ID, text)
    bot.send_message(chat_id, "✅ Buyurtmangiz yuborildi!")


print("🚀 Bot ishga tushdi...")
bot.infinity_polling()
