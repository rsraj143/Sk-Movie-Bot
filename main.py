import telebot
from telebot.types import Message
from flask import Flask, request
import os
import json
import datetime

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# Flask app তৈরি
app = Flask(name)

# movies.json থেকে মুভি লোড
with open("movies.json", "r") as f:
    MOVIES = json.load(f)

# /start command
@bot.message_handler(commands=['start'])
def send_movie(message: Message):
    parts = message.text.split()
    if len(parts) > 1:
        movie_code = parts[1]
    else:
        movie_code = "default"

    bot.send_message(message.chat.id, "🎬 Welcome to Sk Movie Bot!\nPlease wait...")

    # লগ রাখা
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


# Telegram webhook route
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data(as_text=True)
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200


# Home route for UptimeRobot ping
@app.route("/", methods=["GET"])
def home():
    return "✅ Bot is alive!", 200


# সার্ভার চালানো
if name == "main":
    url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"
    bot.remove_webhook()
    bot.set_webhook(url=url)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
