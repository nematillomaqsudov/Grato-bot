import telebot
from telebot import types
import os
import json

TOKEN = os.getenv("TOKEN")
ADMIN_ID = 6877877555

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(msg):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    web_app = types.WebAppInfo("https://gratofood.github.io/miniapp/?v=30")

    markup.add(types.KeyboardButton("🛍 Buyurtma berish", web_app=web_app))

    bot.send_message(msg.chat.id, "Buyurtma berish 👇", reply_markup=markup)


@bot.message_handler(content_types=["web_app_data"])
def webapp(msg):
    chat_id = msg.chat.id

    try:
        data = json.loads(msg.web_app_data.data)
    except:
        return bot.send_message(chat_id, "Xatolik ❌")

    items = data.get("items", [])
    name = data.get("name")
    phone = data.get("phone")
    address = data.get("address")
    location = data.get("location", {})

    lat = location.get("lat")
    lon = location.get("lon")

    if not items:
        return bot.send_message(chat_id, "Savat bo'sh ❌")

    counts = {}
    for i in items:
        counts[i] = counts.get(i, 0) + 1

    text = "🛒 Zakaz:\n\n"
    text += f"👤 {name}\n"
    text += f"📞 +998{phone}\n"
    text += f"📍 {lat},{lon}\n"
    text += f"🏠 {address}\n\n"
    text += f"🗺 https://maps.google.com/?q={lat},{lon}\n\n"

    for item, qty in counts.items():
        text += f"{item} x{qty}\n"

    bot.send_message(ADMIN_ID, text)
    bot.send_message(chat_id, "✅ Yuborildi")

bot.infinity_polling()
