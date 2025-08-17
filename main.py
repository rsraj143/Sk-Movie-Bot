import os
from flask import Flask, request
import telegram

# ✅ Environment থেকে টোকেন নেব
TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN not found in environment variables!")

bot = telegram.Bot(token=TOKEN)

# ✅ Flask App
app = Flask(name)

# Root চেক করার জন্য
@app.route("/")
def home():
    return "Bot is running!"

# ✅ Webhook URL
@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    bot.process_new_updates([update])
    return "ok", 200

# ✅ লোকালি টেস্ট করার জন্য (Render এ লাগবে না)
if name == "main":
    app.run(debug=True)
