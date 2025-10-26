import os
import sys
import telebot
from dotenv import load_dotenv
from user_manager import UserManager
from functions.keyboards import create_start_keyboard, create_gates_keyboard
from functions.messages import format_welcome_message
from commands.handlers import register_command_handlers, register_callback_handler

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_USERNAME = os.getenv('CHANNEL_USERNAME', 'victusxgod')
OWNER_URL = os.getenv('OWNER_URL', 'https://t.me/victus_xd')
WORKERS = int(os.getenv('WORKERS', '16'))
OWNER_ID_1 = int(os.getenv('OWNER_ID_1', '0'))
OWNER_ID_2 = int(os.getenv('OWNER_ID_2', '0'))

if not BOT_TOKEN:
    print("❌ ERROR: BOT_TOKEN environment variable is not set!")
    print("Please set BOT_TOKEN in Render dashboard: Environment → Add Environment Variable")
    sys.exit(1)

if OWNER_ID_1 == 0 or OWNER_ID_2 == 0:
    print("⚠️  WARNING: OWNER_ID_1 or OWNER_ID_2 not set. Admin commands will not work!")
    print("Please set these in Render dashboard: Environment → Add Environment Variable")

bot = telebot.TeleBot(BOT_TOKEN, num_threads=WORKERS)
user_manager = UserManager()

OWNERS = [OWNER_ID_1, OWNER_ID_2]

register_command_handlers(bot, user_manager, OWNERS, CHANNEL_USERNAME, OWNER_URL)
register_callback_handler(bot, user_manager, CHANNEL_USERNAME, OWNER_URL)

def main():
    print(f"🤖 Bot started with {WORKERS} workers")
    print(f"👑 Owners: {OWNER_ID_1}, {OWNER_ID_2}")
    print(f"📢 Channel: @{CHANNEL_USERNAME}")
    print("⚡ Bot is running...")
    
    try:
        bot.infinity_polling(timeout=30, long_polling_timeout=30, skip_pending=True)
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        print("🔄 Restarting bot...")
        main()

if __name__ == '__main__':
    main()
