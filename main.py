from keep_alive import keep_alive
import telebot
from telebot.types import Message
import os
import json
import datetime
import threading
import time

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

with open("movies.json", "r") as f:
    MOVIES = json.load(f)

QUEUE_FILE = "delete_queue.json"

def load_queue():
    if not os.path.exists(QUEUE_FILE):
        return []
    with open(QUEUE_FILE, "r") as f:
        return json.load(f)

def save_queue(data):
    with open(QUEUE_FILE, "w") as f:
        json.dump(data, f)

# ⏳ ২৪ ঘণ্টা delay (86400 sec)
def add_to_queue(chat_id, message_id):
    queue = load_queue()
    delete_time = time.time() + 86400  # 24 hours
    queue.append({
        "chat_id": chat_id,
        "message_id": message_id,
        "delete_at": delete_time
    })
    save_queue(queue)

# 🔁 background checker (optimized)
def delete_worker():
    while True:
        queue = load_queue()
        new_queue = []
        now = time.time()

        for item in queue:
            if now >= item["delete_at"]:
                try:
                    bot.delete_message(item["chat_id"], item["message_id"])
                except Exception as e:
                    print("Delete error:", e)
            else:
                new_queue.append(item)

        save_queue(new_queue)
        time.sleep(30)

threading.Thread(target=delete_worker, daemon=True).start()

@bot.message_handler(commands=['start'])
def send_movie(message: Message):
    parts = message.text.split()
    if len(parts) > 1:
        movie_code = parts[1]
    else:
        movie_code = "default"

    bot.send_message(message.chat.id, "🎬 Welcome to Sk Movie Bot!\nPlease wait...")

    # log system
    user_id = message.chat.id
    username = message.chat.username
    first_name = message.chat.first_name
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_text = f"{now} - {first_name} (@{username}) - ID: {user_id} - Movie: {movie_code}\n"
    with open("log.txt", "a") as f:
        f.write(log_text)

    movie = MOVIES.get(movie_code, MOVIES["default"])
    try:
        sent_msg = bot.copy_message(
            chat_id=message.chat.id,
            from_chat_id=movie["chat_id"],
            message_id=movie["msg_id"]
        )

        # ➕ queue তে save (24 hour delete)
        add_to_queue(message.chat.id, sent_msg.message_id)

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ ভিডিও পাঠানো যায়নি। এরর: {e}")

keep_alive()

print("🚀 Bot running in PRO mode (24 hour auto delete)...")
bot.infinity_polling(timeout=10, long_polling_timeout=5)
