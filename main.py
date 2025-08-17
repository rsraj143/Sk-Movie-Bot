from flask import Flask, request
import telegram
import os

app = Flask(name)

# Environment থেকে Bot Token আনুন
TOKEN = os.environ.get("TOKEN")
bot = telegram.Bot(token=TOKEN)

# Root চেক করার জন্য
@app.route("/")
def home():
    return "✅ Bot is running!", 200

# Webhook Route
@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    # যদি /start কমান্ড দেয়
    if update.message and update.message.text == "/start":
        bot.send_message(chat_id=update.message.chat_id, text="🤖 Bot is Live and Working!")

    return "ok", 200
