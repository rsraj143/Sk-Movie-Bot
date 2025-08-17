from flask import Flask, request
import telebot
import os
import json
import datetime

# টোকেন লোড করা হচ্ছে
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# movies.json ফাইল থেকে মুভির তালিকা লোড করা হচ্ছে
with open("movies.json", "r") as f:
    MOVIES = json.load(f)

# Flask app তৈরি
app = Flask(name)

# /start কমান্ডের জন্য ফাংশন
@bot.message_handler(commands=['start'])
def send_movie(message):
    # কমান্ড থেকে মুভির কোড আলাদা করা
    parts = message.text.split()
    if len(parts) > 1:
        movie_code = parts[1]
    else:
        movie_code = "default"

    bot.send_message(message.chat.id, "🎬 Welcome to Sk Movie Bot!\nPlease wait...")

    # ব্যবহারকারীর তথ্য লগ
    user_id = message.chat.id
    username = message.chat.username
    first_name = message.chat.first_name
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_text = f"{now} - {first_name} (@{username}) - ID: {user_id} - Movie: {movie_code}\n"
    with open("log.txt", "a") as f:
        f.write(log_text)

    # JSON থেকে মুভি পাঠানো
    movie = MOVIES.get(movie_code, MOVIES["default"])
    try:
        bot.copy_message(chat_id=message.chat.id,
                         from_chat_id=movie["chat_id"],
                         message_id=movie["msg_id"])
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ ভিডিও পাঠানো যায়নি। এরর: {e}")


# Render Webhook route
@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200


@app.route('/')
def index():
    return "✅ Bot is running with Webhook!", 200


if name == "main":
    # লোকালি টেস্ট করার জন্য polling (Render-এ চলবে না)
    bot.remove_webhook()
    bot.infinity_polling()
