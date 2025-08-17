import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Flask app for webhook
app = Flask(name)

# Telegram Bot Token from Render Environment (your variable name = TOKEN)
TOKEN = os.getenv("TOKEN")

# Telegram Bot Application
application = Application.builder().token(TOKEN).build()


# --- Command Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running with webhook!")


# Add handlers
application.add_handler(CommandHandler("start", start))


# --- Flask Routes ---
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok", 200


@app.route("/", methods=["GET"])
def home():
    return "Bot is running on Render!", 200


# --- Run Locally (only for debugging, Render uses Gunicorn) ---
if name == "main":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
