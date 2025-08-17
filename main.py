import os
from flask import Flask, request
import telegram

TOKEN = os.getenv("TOKEN")  # Render Environment থেকে নিন
bot = telegram.Bot(token=TOKEN)

app = Flask(name)

@app.route('/')
def home():
    return "Bot is running!"

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    text = update.message.text
    bot.send_message(chat_id=chat_id, text=f"আপনি লিখেছেন: {text}")
    return "ok"

if name == "main":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
