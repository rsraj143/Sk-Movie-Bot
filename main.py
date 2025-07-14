from keep_alive import keep_alive
import telebot
from telebot.types import Message
import os
import json
import datetime

# টোকেন লোড করা হচ্ছে
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# movies.json ফাইল থেকে মুভির তালিকা লোড করা হচ্ছে
with open("movies.json", "r") as f:
    MOVIES = json.load(f)

# /start কমান্ডের জন্য ফাংশন
@bot.message_handler(commands=['start'])
def send_movie(message: Message):
    # কমান্ড থেকে মুভির কোড আলাদা করার সঠিক নিয়ম
    try:
        # message.text হলো সম্পূর্ণ মেসেজ (যেমন: "/start paap")
        # .split() এটিকে দুটি অংশে ভাগ করে: ["/start", "paap"]
        # [1] দিয়ে আমরা দ্বিতীয় অংশটি (অর্থাৎ "paap") নিচ্ছি
        movie_code = message.text.split()[1]
    except IndexError:
        # যদি ব্যবহারকারী শুধু "/start" লেখে, তাহলে কোনো দ্বিতীয় অংশ থাকবে না
        # তাই IndexError হবে এবং আমরা ডিফল্ট কোড ব্যবহার করব
        movie_code = "default"

    bot.send_message(message.chat.id, "🎬 Welcome to Sk Movie Bot!\nPlease wait...")

    # ব্যবহারকারীর তথ্য লগ করা হচ্ছে
    user_id = message.chat.id
    username = message.chat.username
    first_name = message.chat.first_name
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_text = f"{now} - {first_name} (@{username}) - ID: {user_id} - Movie: {movie_code}\n"
    with open("log.txt", "a") as f:
        f.write(log_text)

    # JSON থেকে মুভি পাঠানো হচ্ছে
    # .get() ফাংশন movie_code খুঁজে না পেলে ডিফল্ট মুভি পাঠায়
    movie = MOVIES.get(movie_code, MOVIES["default"])
    try:
        bot.copy_message(chat_id=message.chat.id,
                         from_chat_id=movie["chat_id"],
                         message_id=movie["msg_id"])
    except Exception as e:
        bot.send_message(message.chat.id, "❌ ভিডিও পাঠানো যায়নি, পরে আবার চেষ্টা করুন।")

# keep_alive ফাংশনটি চালু করা হচ্ছে যাতে Render-এর ওয়েব সার্ভিস চালু থাকে
keep_alive()

# বট সবসময় চালু রাখার জন্য
print("✅ Bot is running...")
bot.infinity_polling(timeout=10, long_polling_timeout=5)
