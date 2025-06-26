import telebot
from telebot.types import Message
import os
from dotenv import load_dotenv
import json
import datetime

# Load token
load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# Load movies from external file
with open("movies.json", "r") as f:
    MOVIES = json.load(f)

@bot.message_handler(commands=['start'])
def send_movie(message: Message):
    args = message.text.split()
    movie_code = args[1] if len(args) > 1 else "default"

    bot.send_message(message.chat.id, "🎬 Welcome to Sk Movie Bot!\nPlease wait...")

    # User log
    user_id = message.chat.id
    username = message.chat.username
    first_name = message.chat.first_name
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_text = f"{now} - {first_name} (@{username}) - ID: {user_id} - Movie: {movie_code}\n"
    with open("log.txt", "a") as f:
        f.write(log_text)

    # Send movie from JSON
    movie = MOVIES.get(movie_code, MOVIES["default"])
    try:
        bot.copy_message(chat_id=message.chat.id,
                         from_chat_id=movie["chat_id"],
                         message_id=movie["msg_id"])
        # প্রমোশনাল মেসেজটি এইখানে ছিল, এখন সরানো হয়েছে
    except Exception as e:
        bot.send_message(message.chat.id, "❌ ভিডিও পাঠানো যায়নি, পরে আবার চেষ্টা করুন।")

# Keep bot alive
print("✅ Bot is running...")
bot.infinity_polling(timeout=10, long_polling_timeout=5)
