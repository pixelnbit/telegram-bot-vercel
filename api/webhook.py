import os
import telebot
from flask import Flask, request
from user_manager import UserManager
from commands.handlers import register_command_handlers, register_callback_handler

# Load environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_USERNAME = os.getenv('CHANNEL_USERNAME', 'victusxgod')
OWNER_URL = os.getenv('OWNER_URL', 'https://t.me/victus_xd')
OWNER_ID_1 = int(os.getenv('OWNER_ID_1', '0'))
OWNER_ID_2 = int(os.getenv('OWNER_ID_2', '0'))
WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
user_manager = UserManager()

OWNERS = [OWNER_ID_1, OWNER_ID_2]

# Register handlers
register_command_handlers(bot, user_manager, OWNERS, CHANNEL_USERNAME, OWNER_URL)
register_callback_handler(bot, user_manager, CHANNEL_USERNAME, OWNER_URL)

# Create Flask app
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Telegram Bot is running on Vercel!", 200

@app.route('/api/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return '', 403

@app.route('/api/setWebhook', methods=['GET'])
def set_webhook():
    webhook_url = f"{WEBHOOK_URL}/api/webhook"
    bot.remove_webhook()
    success = bot.set_webhook(url=webhook_url)
    if success:
        return f"Webhook set to {webhook_url}", 200
    else:
        return "Failed to set webhook", 500

# For Vercel serverless
def handler(request):
    return app(request.environ, lambda *args: None)
