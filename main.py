import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# লগ সেটআপ
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(name)

# Render এ রাখা TOKEN environment থেকে পড়বে
TOKEN = os.getenv("TOKEN")

# Flask app
app = Flask(name)

# Telegram bot application
application = Application.builder().token(TOKEN).build()


# Start command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("✅ Bot is running with webhook!")


# Command হ্যান্ডলার যোগ করা
application.add_handler(CommandHandler("start", start))


# Flask route for webhook
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"


# Render-এর হেলথ চেক রুট
@app.route("/")
def index():
    return "Bot is running via webhook!"


if name == "main":
    # লোকাল টেস্ট করার জন্য
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
