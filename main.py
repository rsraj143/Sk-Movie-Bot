from flask import Flask, request
import os
import telegram
import json

TOKEN = os.getenv("TOKEN")  # Render এ Environment variable এ TOKEN রাখবেন
bot = telegram.Bot(token=TOKEN)

app = Flask(name)

# মুভি লোড ফাংশন
def load_movies():
    try:
        with open("movie.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

@app.route("/")
def home():
    return "Bot is running!"

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    if update.message and update.message.text:
        text = update.message.text.strip().lower()
        chat_id = update.message.chat.id

        movies = load_movies()
        result = [m for m in movies if text in m["title"].lower()]

        if result:
            reply = "\n".join([f"🎬 {m['title']} - {m['link']}" for m in result])
        else:
            reply = "❌ কিছু পাওয়া যায়নি!"

        bot.send_message(chat_id=chat_id, text=reply)

    return "ok"

if name == "main":
    app.run(host="0.0.0.0", port=5000)
