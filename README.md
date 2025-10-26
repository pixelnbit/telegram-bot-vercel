# Telegram Bot - Render Deployment

A powerful Telegram bot for card checking, deployed on Render.

## Features

- 🔐 Card validation and checking
- 💳 Multiple payment gateways support
- 👥 User management system
- 🎯 Premium user features
- 🔄 BIN lookup functionality

## Deployment on Render

### Quick Deploy

1. **Fork or push this repo to GitHub**

2. **Go to [render.com](https://render.com)** and sign up/login

3. **Create a New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `telegram-bot-vercel` repository

4. **Configure the service:**
   - **Name:** telegram-bot (or your choice)
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python main.py`
   - **Plan:** Free

5. **Add Environment Variables:**
   - `BOT_TOKEN` - Your bot token from @BotFather
   - `CHANNEL_USERNAME` - Your channel (e.g., victusxgod)
   - `OWNER_URL` - Owner URL (e.g., https://t.me/victus_xd)
   - `OWNER_ID_1` - First owner's Telegram user ID
   - `OWNER_ID_2` - Second owner's Telegram user ID
   - `WORKERS` - Number of workers (default: 16)

6. **Click "Create Web Service"**

7. **Wait for deployment** - Render will build and start your bot automatically!

### Alternative: Deploy with Blueprint

Use the `render.yaml` file for automatic deployment.

## Local Development

Create a `.env` file:

```env
BOT_TOKEN=your_bot_token_here
CHANNEL_USERNAME=your_channel
OWNER_URL=https://t.me/your_username
OWNER_ID_1=123456789
OWNER_ID_2=987654321
WORKERS=16
```

Run locally:

```bash
pip install -r requirements.txt
python main.py
```

## Commands

### User Commands
- `/start` - Start the bot and register
- `/kill cc|mm|yy|cvv` - Check card using CC Killer gateway
- `/chk cc|mm|yy|cvv` - Check card using Braintree gateway

### Admin Commands
- `/setpremium <user_id>` - Grant premium access
- `/removepremium <user_id>` - Remove premium access
- `/cup <cookies>` - Update cookies for Braintree checker

## Project Structure

```
telegram-bot/
├── commands/
│   ├── __init__.py
│   └── handlers.py         # Command handlers
├── functions/
│   ├── __init__.py
│   ├── bin_lookup.py       # BIN information lookup
│   ├── braintree_checker.py # Braintree gateway checker
│   ├── cc_killer.py        # CC Killer gateway
│   ├── keyboards.py        # Telegram keyboards
│   └── messages.py         # Message templates
├── main.py                 # Main bot file
├── user_manager.py         # User management
├── users.json              # User database
├── requirements.txt        # Python dependencies
├── Procfile               # Render process file
├── render.yaml            # Render configuration
└── README.md              # This file
```

## How to Get Telegram User ID

Send a message to [@userinfobot](https://t.me/userinfobot) on Telegram.

## Support

For support, contact the bot owner or join our channel.

## License

This project is for educational purposes only.
