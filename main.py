import telebot
from telebot.types import Message
import os
import json
import datetime
from flask import Flask, request

# Telegram Bot Token (Render → Environment Variables এ TOKEN দিতে হবে)
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# Flask app তৈরি
app = Flask(name)

# movies.json ফাইল থেকে মুভির তালিকা লোড করা হচ্ছে
with open("movies.json", "r") as f:
    MOVIES = json.load(f)

# /start কমান্ড
@bot.message_handler(commands=['start'])
def send_movie(message: Message):
    # movie code বের করা
    parts = message.text.split()
    if len(parts) > 1:
        movie_code = parts[1]
    else:
        movie_code = "default"

    bot.send_message(message.chat.id, "🎬 Welcome to Sk Movie Bot!\nPlease wait...")

    # লগ ফাইলে ব্যবহারকারীর তথ্য লেখা
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

# Telegram → আমাদের সার্ভারে আপডেট পাঠাবে
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

# Root route → Webhook সেট করা
@app.route("/", methods=["GET"])
def index():
    bot.remove_webhook()
    bot.set_webhook(url=f"https://<your-app-name>.onrender.com/{TOKEN}")  # ⚠️ এখানে আপনার Render app name বসান
    return "✅ Webhook set successfully!", 200

# Render সার্ভার চালু
if name == "main":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
