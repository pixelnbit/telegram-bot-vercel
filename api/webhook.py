import os
import sys
import json

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import telebot
from telebot.types import Update
from user_manager import UserManager
from commands.handlers import register_command_handlers, register_callback_handler

# Load environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN', '')
CHANNEL_USERNAME = os.getenv('CHANNEL_USERNAME', 'victusxgod')
OWNER_URL = os.getenv('OWNER_URL', 'https://t.me/victus_xd')
OWNER_ID_1 = int(os.getenv('OWNER_ID_1', '0'))
OWNER_ID_2 = int(os.getenv('OWNER_ID_2', '0'))
WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')

# Initialize bot
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set")

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
user_manager = UserManager()

OWNERS = [OWNER_ID_1, OWNER_ID_2]

# Register handlers
register_command_handlers(bot, user_manager, OWNERS, CHANNEL_USERNAME, OWNER_URL)
register_callback_handler(bot, user_manager, CHANNEL_USERNAME, OWNER_URL)

# Vercel serverless handler
def handler(event, context):
    try:
        # Handle different paths
        path = event.get('path', '/')
        method = event.get('httpMethod', 'GET')
        
        # Root path
        if path == '/' or path == '/api':
            return {
                'statusCode': 200,
                'body': 'Telegram Bot is running on Vercel!'
            }
        
        # Set webhook endpoint
        if path == '/api/setWebhook' and method == 'GET':
            webhook_url = f"{WEBHOOK_URL}/api/webhook"
            bot.remove_webhook()
            success = bot.set_webhook(url=webhook_url)
            if success:
                return {
                    'statusCode': 200,
                    'body': f'Webhook set to {webhook_url}'
                }
            else:
                return {
                    'statusCode': 500,
                    'body': 'Failed to set webhook'
                }
        
        # Webhook endpoint - receive updates from Telegram
        if path == '/api/webhook' and method == 'POST':
            body = event.get('body', '')
            if body:
                try:
                    update = Update.de_json(body)
                    if update:
                        bot.process_new_updates([update])
                except Exception as e:
                    print(f"Update processing error: {str(e)}")
                return {
                    'statusCode': 200,
                    'body': 'OK'
                }
            else:
                return {
                    'statusCode': 400,
                    'body': 'No body'
                }
        
        # Default response
        return {
            'statusCode': 404,
            'body': 'Not Found'
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }
