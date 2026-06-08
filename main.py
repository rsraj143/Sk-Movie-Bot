from keep_alive import keep_alive
import telebot
from telebot.types import Message
import os
import json
import datetime

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

with open("movies.json", "r") as f:
    MOVIES = json.load(f)

@bot.message_handler(commands=['start'])
def send_movie(message: Message):
    parts = message.text.split()
    if len(parts) > 1:
        movie_code = parts[1]
    else:
        movie_code = "default"

    bot.send_message(message.chat.id, "🎬 Welcome to Sk Movie Bot!\nPlease wait...")

    # Log system
    user_id = message.chat.id
    username = message.chat.username
    first_name = message.chat.first_name
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_text = f"{now} - {first_name} (@{username}) - ID: {user_id} - Movie: {movie_code}\n"

    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(log_text)

    movie = MOVIES.get(movie_code, MOVIES["default"])

    try:
        bot.copy_message(
            chat_id=message.chat.id,
            from_chat_id=movie["chat_id"],
            message_id=movie["msg_id"]
        )
    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"❌ ভিডিও পাঠানো যায়নি। এরর: {e}"
        )

keep_alive()

print("🚀 Bot running...")
bot.infinity_polling(timeout=10, long_polling_timeout=5)
