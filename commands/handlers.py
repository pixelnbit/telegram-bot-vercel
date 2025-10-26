from telebot import types
from functions.keyboards import create_start_keyboard, create_gates_keyboard
from functions.messages import format_welcome_message
from functions.cc_killer import check_card as kill_card
from functions.braintree_checker import check_card as braintree_check
from functions.bin_lookup import get_bin_info, get_country_flag
import time
import re
import os

def register_command_handlers(bot, user_manager, owners, channel_username, owner_url):
    
    @bot.message_handler(commands=['start'])
    def start_handler(message):
        try:
            user_id = message.from_user.id
            username = message.from_user.username
            first_name = str(message.from_user.first_name).encode('utf-16', 'surrogatepass').decode('utf-16', 'ignore') if message.from_user.first_name else 'User'
            last_name = message.from_user.last_name
            
            print(f"[DEBUG] /start command from user {user_id} ({first_name})")
            
            is_registered = user_manager.is_registered(user_id)
            
            welcome_msg = format_welcome_message(first_name, is_registered, channel_username)
            markup = create_start_keyboard(is_registered)
            
            try:
                with open('thumbnail.png', 'rb') as photo:
                    bot.send_photo(
                        message.chat.id,
                        photo,
                        caption=welcome_msg,
                        parse_mode='Markdown',
                        reply_markup=markup
                    )
                    print(f"[DEBUG] Start message sent with photo to {user_id}")
            except Exception as e:
                print(f"[ERROR] Failed to send photo: {e}")
                bot.send_message(
                    message.chat.id,
                    welcome_msg,
                    parse_mode='Markdown',
                    reply_markup=markup,
                    disable_web_page_preview=True
                )
                print(f"[DEBUG] Start message sent without photo to {user_id}")
        except Exception as e:
            print(f"[ERROR] Start handler error: {e}")
            import traceback
            traceback.print_exc()
            bot.send_message(message.chat.id, "⚠️ 𝗔𝗻 𝗲𝗿𝗿𝗼𝗿 𝗼𝗰𝗰𝘂𝗿𝗿𝗲𝗱. 𝗣𝗹𝗲𝗮𝘀𝗲 𝘁𝗿𝘆 𝗮𝗴𝗮𝗶𝗻.")
    
    @bot.message_handler(commands=['setpremium', 'removepremium', 'cup'])
    def owner_commands_handler(message):
        try:
            user_id = message.from_user.id
            
            if user_id not in owners:
                return
            
            text = message.text.strip()
            
            if text.startswith('/setpremium '):
                try:
                    target_id = int(text.split()[1])
                    if user_manager.set_premium(target_id, True):
                        bot.reply_to(message, f"✅ 𝗨𝘀𝗲𝗿 `{target_id}` 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗽𝗿𝗼𝗺𝗼𝘁𝗲𝗱 𝘁𝗼 𝗽𝗿𝗲𝗺𝗶𝘂𝗺!", parse_mode='Markdown')
                    else:
                        bot.reply_to(message, f"⚠️ 𝗨𝘀𝗲𝗿 `{target_id}` 𝗻𝗼𝘁 𝗳𝗼𝘂𝗻𝗱!", parse_mode='Markdown')
                except:
                    bot.reply_to(message, "⚠️ 𝗨𝘀𝗮𝗴𝗲: /setpremium <user_id>", parse_mode='Markdown')
            
            elif text.startswith('/removepremium '):
                try:
                    target_id = int(text.split()[1])
                    if user_manager.set_premium(target_id, False):
                        bot.reply_to(message, f"✅ 𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗥𝗲𝗺𝗼𝘃𝗲𝗱 𝗙𝗿𝗼𝗺 `{target_id}`!", parse_mode='Markdown')
                    else:
                        bot.reply_to(message, f"⚠️ 𝗨𝘀𝗲𝗿 `{target_id}` 𝗻𝗼𝘁 𝗳𝗼𝘂𝗻𝗱!", parse_mode='Markdown')
                except:
                    bot.reply_to(message, "⚠️ 𝗨𝘀𝗮𝗴𝗲: /removepremium <user_id>", parse_mode='Markdown')
            
            elif text.startswith('/cup '):
                try:
                    # Extract cookies from command
                    new_cookies = text.split('/cup ', 1)[1].strip()
                    
                    if not new_cookies:
                        bot.reply_to(message, "⚠️ 𝗨𝘀𝗮𝗴𝗲: /cup <cookies>", parse_mode='Markdown')
                        return
                    
                    braintree_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'functions', 'braintree_checker.py')
                    
                    with open(braintree_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Parse the new cookies and update the cookies dictionary in the file
                    cookie_pairs = {}
                    for cookie in new_cookies.split(';'):
                        if '=' in cookie:
                            key, value = cookie.split('=', 1)
                            cookie_pairs[key.strip()] = value.strip()
                    
                    # Update each cookie in the file
                    updated_content = content
                    for key, value in cookie_pairs.items():
                        # Escape special regex characters in the key
                        escaped_key = re.escape(key)
                        pattern = rf"'{escaped_key}':\s*'[^']*'"
                        replacement = f"'{key}': '{value}'"
                        updated_content = re.sub(pattern, replacement, updated_content)
                    
                    with open(braintree_path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    
                    bot.reply_to(message, f"✅ 𝗖𝗼𝗼𝗸𝗶𝗲𝘀 𝘂𝗽𝗱𝗮𝘁𝗲𝗱 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆!\n\n𝗨𝗽𝗱𝗮𝘁𝗲𝗱 {len(cookie_pairs)} 𝗰𝗼𝗼𝗸𝗶𝗲(𝘀)", parse_mode='Markdown')
                except Exception as e:
                    bot.reply_to(message, f"⚠️ 𝗘𝗿𝗿𝗼𝗿 𝘂𝗽𝗱𝗮𝘁𝗶𝗻𝗴 𝗰𝗼𝗼𝗸𝗶𝗲𝘀: {str(e)}", parse_mode='Markdown')
                    print(f"[ERROR] Cookie update error: {e}")
                    import traceback
                    traceback.print_exc()
        except Exception as e:
            pass
    
    @bot.message_handler(func=lambda message: message.text and message.text.startswith('/kill '))
    def kill_handler(message):
        try:
            user_id = message.from_user.id
            username = message.from_user.username if message.from_user.username else "Unknown"
            
            if not user_manager.is_registered(user_id):
                bot.reply_to(message, "⚠️ 𝗣𝗹𝗲𝗮𝘀𝗲 𝗿𝗲𝗴𝗶𝘀𝘁𝗲𝗿 𝗳𝗶𝗿𝘀𝘁 𝘂𝘀𝗶𝗻𝗴 /start")
                return
            
            print(f"[DEBUG] /kill command from user {user_id}")
            
            text = message.text.strip()
            parts = text.split(' ', 1)
            
            if len(parts) < 2 or not parts[1].strip():
                bot.reply_to(message, "⚠️ 𝗨𝘀𝗮𝗴𝗲: `/kill cc|mm|yy|cvv`", parse_mode='Markdown')
                return
            
            card_input = parts[1]
            for sep in ['|', ':', '/', '\\']:
                if sep in card_input:
                    card_data = card_input.split(sep)
                    break
            else:
                bot.reply_to(message, "⚠️ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗳𝗼𝗿𝗺𝗮𝘁! 𝗨𝘀𝗲: `/kill cc|mm|yy|cvv`", parse_mode='Markdown')
                return
            
            if len(card_data) < 4:
                bot.reply_to(message, "⚠️ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗳𝗼𝗿𝗺𝗮𝘁! 𝗨𝘀𝗲: `/kill cc|mm|yy|cvv`", parse_mode='Markdown')
                return
            
            cc = card_data[0].strip()
            month = card_data[1].strip().zfill(2)
            year = card_data[2].strip()
            if len(year) == 2:
                year = f"20{year}"
            cvv = card_data[3].strip()
            
            if not cc.isdigit() or len(cc) not in [15, 16]:
                bot.reply_to(message, "⚠️ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗰𝗮𝗿𝗱 𝗻𝘂𝗺𝗯𝗲𝗿!")
                return
            
            bin_number = cc[:6]
            bin_info = get_bin_info(bin_number)
            flag = get_country_flag(bin_info['country_code'])
            
            channel_link = f"https://t.me/{channel_username}"
            
            card_display = f"{cc}:{month}:{year}:{cvv}"
            
            initial_msg = f"""[𓉘❀𓉝]({channel_link}) 𝗖𝗮𝗿𝗱 ⇾ `{card_display}`
[𓉘❀𓉝]({channel_link}) 𝗦𝘁𝗮𝘁𝘂𝘀 ⇾ 𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴... ⏳

[𓉘❀𓉝]({channel_link}) 𝗕𝗶𝗻 ⇾ `{bin_number}`
[𓉘❀𓉝]({channel_link}) 𝗜𝘀𝘀𝘂𝗲𝗿 ⇾ {bin_info['bank']}
[𓉘❀𓉝]({channel_link}) 𝗜𝗻𝗳𝗼 ⇾ {bin_info['brand']} - {bin_info['type']} - {bin_info['level']}
[𓉘❀𓉝]({channel_link}) 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 ⇾ {bin_info['country']} [{flag}]
[𓉘❀𓉝]({channel_link}) 𝗕𝗹𝗼𝗰𝗸𝗲𝗱 ⇾ {bin_info['prepaid']}"""
            
            thumbnail_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'thumbnail.png')
            with open(thumbnail_path, 'rb') as photo:
                status_msg = bot.send_photo(message.chat.id, photo, caption=initial_msg, parse_mode='Markdown', reply_to_message_id=message.message_id)
            
            start_time = time.time()
            
            card_info = {
                'cc': cc,
                'month': month,
                'year': year,
                'cvv': cvv
            }
            
            result = kill_card(card_info)
            
            elapsed_time = int(time.time() - start_time)
            
            user_manager.update_user_checks(user_id)
            
            if result['status'] == 'killed':
                status_display = "𝗗𝗘𝗔𝗗"
                response_text = "Card Killed Successfully! ✅"
            elif result['status'] == 'live':
                status_display = "𝗟𝗜𝗩𝗘"
                response_text = "Card is still alive! ⚠️"
            else:
                status_display = "𝗘𝗥𝗥𝗢𝗥"
                response_text = result.get('message', 'Unknown error')
            
            response_text = response_text.replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace('`', '\\`')
            
            final_msg = f"""[𓉘❀𓉝]({channel_link}) 𝗖𝗮𝗿𝗱 ⇾ `{card_display}`
[𓉘❀𓉝]({channel_link}) 𝗦𝘁𝗮𝘁𝘂𝘀 ⇾ {status_display}
[𓉘❀𓉝]({channel_link}) 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 ⇾ `{response_text}`
[𓉘❀𓉝]({channel_link}) 𝗚𝗮𝘁𝗲𝘄𝗮𝘆 ⇾ `CC Killer`

[𓉘❀𓉝]({channel_link}) 𝗕𝗶𝗻 ⇾ `{bin_number}`
[𓉘❀𓉝]({channel_link}) 𝗜𝘀𝘀𝘂𝗲𝗿 ⇾ `{bin_info['bank']}`
[𓉘❀𓉝]({channel_link}) 𝗜𝗻𝗳𝗼 ⇾ `{bin_info['brand']} - {bin_info['type']} - {bin_info['level']}`
[𓉘❀𓉝]({channel_link}) 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 ⇾ `{bin_info['country']}` {bin_info.get('country_flag', flag)}
[𓉘❀𓉝]({channel_link}) 𝗕𝗹𝗼𝗰𝗸𝗲𝗱 ⇾ `{bin_info['prepaid']}`

[𓉘❀𓉝]({channel_link}) 𝗧𝗶𝗺𝗲 𝗧𝗮𝗸𝗲𝗻 ⇾ `{elapsed_time}s`
[𓉘❀𓉝]({channel_link}) 𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 ⇾ `{username}`"""
            
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton('📢 Channel', url=channel_link),
                types.InlineKeyboardButton('👑 Owner', url=owner_url)
            )
            
            bot.edit_message_caption(final_msg, status_msg.chat.id, status_msg.message_id, parse_mode='Markdown', reply_markup=markup)
            
        except Exception as e:
            print(f"[ERROR] Kill command error: {e}")
            import traceback
            traceback.print_exc()
            bot.reply_to(message, "⚠️ 𝗔𝗻 𝗲𝗿𝗿𝗼𝗿 𝗼𝗰𝗰𝘂𝗿𝗿𝗲𝗱!")
    
    @bot.message_handler(func=lambda message: message.text and message.text.startswith('/chk '))
    def chk_handler(message):
        try:
            user_id = message.from_user.id
            username = message.from_user.username if message.from_user.username else "Unknown"
            
            if not user_manager.is_registered(user_id):
                bot.reply_to(message, "⚠️ 𝗣𝗹𝗲𝗮𝘀𝗲 𝗿𝗲𝗴𝗶𝘀𝘁𝗲𝗿 𝗳𝗶𝗿𝘀𝘁 𝘂𝘀𝗶𝗻𝗴 /start")
                return
            
            print(f"[DEBUG] /chk command from user {user_id}")
            
            text = message.text.strip()
            parts = text.split(' ', 1)
            
            if len(parts) < 2 or not parts[1].strip():
                bot.reply_to(message, "⚠️ 𝗨𝘀𝗮𝗴𝗲: `/chk cc|mm|yy|cvv`", parse_mode='Markdown')
                return
            
            card_input = parts[1]
            for sep in ['|', ':', '/', '\\']:
                if sep in card_input:
                    card_data = card_input.split(sep)
                    break
            else:
                bot.reply_to(message, "⚠️ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗳𝗼𝗿𝗺𝗮𝘁! 𝗨𝘀𝗲: `/chk cc|mm|yy|cvv`", parse_mode='Markdown')
                return
            
            if len(card_data) < 4:
                bot.reply_to(message, "⚠️ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗳𝗼𝗿𝗺𝗮𝘁! 𝗨𝘀𝗲: `/chk cc|mm|yy|cvv`", parse_mode='Markdown')
                return
            
            cc = card_data[0].strip()
            month = card_data[1].strip().zfill(2)
            year = card_data[2].strip()
            if len(year) == 2:
                year = f"20{year}"
            cvv = card_data[3].strip()
            
            if not cc.isdigit() or len(cc) not in [15, 16]:
                bot.reply_to(message, "⚠️ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗰𝗮𝗿𝗱 𝗻𝘂𝗺𝗯𝗲𝗿!")
                return
            
            bin_number = cc[:6]
            bin_info = get_bin_info(bin_number)
            flag = get_country_flag(bin_info['country_code'])
            
            channel_link = f"https://t.me/{channel_username}"
            
            card_display = f"{cc}:{month}:{year}:{cvv}"
            
            initial_msg = f"""[𓉘❀𓉝]({channel_link}) 𝗖𝗮𝗿𝗱 ⇾ `{card_display}`
[𓉘❀𓉝]({channel_link}) 𝗦𝘁𝗮𝘁𝘂𝘀 ⇾ 𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴... ⏳

[𓉘❀𓉝]({channel_link}) 𝗕𝗶𝗻 ⇾ `{bin_number}`
[𓉘❀𓉝]({channel_link}) 𝗜𝘀𝘀𝘂𝗲𝗿 ⇾ {bin_info['bank']}
[𓉘❀𓉝]({channel_link}) 𝗜𝗻𝗳𝗼 ⇾ {bin_info['brand']} - {bin_info['type']} - {bin_info['level']}
[𓉘❀𓉝]({channel_link}) 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 ⇾ {bin_info['country']} [{flag}]
[𓉘❀𓉝]({channel_link}) 𝗕𝗹𝗼𝗰𝗸𝗲𝗱 ⇾ {bin_info['prepaid']}"""
            
            thumbnail_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'thumbnail.png')
            with open(thumbnail_path, 'rb') as photo:
                status_msg = bot.send_photo(message.chat.id, photo, caption=initial_msg, parse_mode='Markdown', reply_to_message_id=message.message_id)
            
            start_time = time.time()
            
            result = braintree_check(cc, month, year, cvv)
            
            elapsed_time = int(time.time() - start_time)
            
            user_manager.update_user_checks(user_id)
            
            if result['status'] == 'approved':
                status_display = "𝗔𝗣𝗣𝗥𝗢𝗩𝗘𝗗 ✅"
                response_text = result.get('message', 'Card Approved!')
            elif result['status'] == 'declined':
                status_display = "𝗗𝗘𝗖𝗟𝗜𝗡𝗘𝗗 ❌"
                response_text = result.get('message', 'Card Declined')
            else:
                status_display = "𝗘𝗥𝗥𝗢𝗥 ⚠️"
                response_text = result.get('message', 'Unknown error')
            
            response_text = response_text.replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace('`', '\\`')
            
            final_msg = f"""[𓉘❀𓉝]({channel_link}) 𝗖𝗮𝗿𝗱 ⇾ `{card_display}`
[𓉘❀𓉝]({channel_link}) 𝗦𝘁𝗮𝘁𝘂𝘀 ⇾ {status_display}
[𓉘❀𓉝]({channel_link}) 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 ⇾ `{response_text}`
[𓉘❀𓉝]({channel_link}) 𝗚𝗮𝘁𝗲𝘄𝗮𝘆 ⇾ `Braintree Auth`

[𓉘❀𓉝]({channel_link}) 𝗕𝗶𝗻 ⇾ `{bin_number}`
[𓉘❀𓉝]({channel_link}) 𝗜𝘀𝘀𝘂𝗲𝗿 ⇾ `{bin_info['bank']}`
[𓉘❀𓉝]({channel_link}) 𝗜𝗻𝗳𝗼 ⇾ `{bin_info['brand']} - {bin_info['type']} - {bin_info['level']}`
[𓉘❀𓉝]({channel_link}) 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 ⇾ `{bin_info['country']}` {bin_info.get('country_flag', flag)}
[𓉘❀𓉝]({channel_link}) 𝗕𝗹𝗼𝗰𝗸𝗲𝗱 ⇾ `{bin_info['prepaid']}`

[𓉘❀𓉝]({channel_link}) 𝗧𝗶𝗺𝗲 𝗧𝗮𝗸𝗲𝗻 ⇾ `{elapsed_time}s`
[𓉘❀𓉝]({channel_link}) 𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 ⇾ `{username}`"""
            
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton('📢 Channel', url=channel_link),
                types.InlineKeyboardButton('👑 Owner', url=owner_url)
            )
            
            bot.edit_message_caption(final_msg, status_msg.chat.id, status_msg.message_id, parse_mode='Markdown', reply_markup=markup)
            
        except Exception as e:
            print(f"[ERROR] Chk command error: {e}")
            import traceback
            traceback.print_exc()
            bot.reply_to(message, "⚠️ 𝗔𝗻 𝗲𝗿𝗿𝗼𝗿 𝗼𝗰𝗰𝘂𝗿𝗿𝗲𝗱!")
    
    @bot.message_handler(commands=['kill'])
    def kill_no_card_handler(message):
        bot.reply_to(message, "⚠️ 𝗨𝘀𝗮𝗴𝗲: `/kill cc|mm|yy|cvv`", parse_mode='Markdown')
    
    @bot.message_handler(commands=['chk'])
    def chk_no_card_handler(message):
        bot.reply_to(message, "⚠️ 𝗨𝘀𝗮𝗴𝗲: `/chk cc|mm|yy|cvv`", parse_mode='Markdown')

def register_callback_handler(bot, user_manager, channel_username, owner_url):
    
    @bot.callback_query_handler(func=lambda call: True)
    def callback_handler(call):
        try:
            user_id = call.from_user.id
            print(f"[DEBUG] Callback received: {call.data} from user {user_id}")
            
            if call.data == 'register':
                if user_manager.is_registered(user_id):
                    bot.answer_callback_query(call.id, "✅ 𝗬𝗼𝘂 𝗮𝗿𝗲 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗿𝗲𝗴𝗶𝘀𝘁𝗲𝗿𝗲𝗱!")
                    return
                
                username = call.from_user.username
                first_name = str(call.from_user.first_name).encode('utf-16', 'surrogatepass').decode('utf-16', 'ignore') if call.from_user.first_name else 'User'
                last_name = call.from_user.last_name
                
                success = user_manager.register_user(user_id, username, first_name, last_name)
                
                print(f"[DEBUG] Registration attempt for user {user_id}: {success}")
                
                if success:
                    channel_link = f"https://t.me/{channel_username}"
                    success_msg = f"""[𓉘❀𓉝]({channel_link}) 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝘁𝗶𝗼𝗻 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹!

[𓉘❀𓉝]({channel_link}) ✅ 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 **{first_name}**

[𓉘❀𓉝]({channel_link}) 𝗬𝗼𝘂 𝗰𝗮𝗻 𝗻𝗼𝘄 𝗮𝗰𝗰𝗲𝘀𝘀 𝗮𝗹𝗹 𝗳𝗲𝗮𝘁𝘂𝗿𝗲𝘀"""
                    
                    markup = create_start_keyboard(True)
                    try:
                        with open('thumbnail.png', 'rb') as photo:
                            bot.delete_message(call.message.chat.id, call.message.message_id)
                            bot.send_photo(
                                call.message.chat.id,
                                photo,
                                caption=success_msg,
                                parse_mode='Markdown',
                                reply_markup=markup
                            )
                    except:
                        try:
                            bot.edit_message_caption(
                                success_msg,
                                call.message.chat.id,
                                call.message.message_id,
                                parse_mode='Markdown',
                                reply_markup=markup
                            )
                        except:
                            bot.edit_message_text(
                                success_msg,
                                call.message.chat.id,
                                call.message.message_id,
                                parse_mode='Markdown',
                                reply_markup=markup,
                                disable_web_page_preview=True
                            )
                    bot.answer_callback_query(call.id, "✅ 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝘁𝗶𝗼𝗻 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹!")
                else:
                    bot.answer_callback_query(call.id, "⚠️ 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝘁𝗶𝗼𝗻 𝗳𝗮𝗶𝗹𝗲𝗱. 𝗧𝗿𝘆 𝗮𝗴𝗮𝗶𝗻.")
            
            elif call.data == 'profile':
                user_data = user_manager.get_user(user_id)
                
                if not user_data:
                    bot.answer_callback_query(call.id, "⚠️ 𝗣𝗹𝗲𝗮𝘀𝗲 𝗿𝗲𝗴𝗶𝘀𝘁𝗲𝗿 𝗳𝗶𝗿𝘀𝘁!")
                    return
                
                try:
                    channel_link = f"https://t.me/{channel_username}"
                    first_name_safe = str(user_data['first_name']).encode('utf-16', 'surrogatepass').decode('utf-16', 'ignore') if user_data['first_name'] else 'N/A'
                    status = "💎 𝗣𝗿𝗲𝗺𝗶𝘂𝗺" if user_data.get('is_premium', False) else "🆓 𝗙𝗿𝗲𝗲"
                    
                    profile_msg_plain = f"""[𓉘❀𓉝]({channel_link}) 𝗣𝗿𝗼𝗳𝗶𝗹𝗲

[𓉘❀𓉝]({channel_link}) 𝗡𝗮𝗺𝗲: {first_name_safe}
[𓉘❀𓉝]({channel_link}) 𝗨𝗜𝗗: `{user_data['user_id']}`
[𓉘❀𓉝]({channel_link}) 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲: `@{user_data['username']}`
[𓉘❀𓉝]({channel_link}) 𝗥𝗲𝗴𝗶𝘀𝘁𝗲𝗿𝗲𝗱: `{user_data['registered_at']}`
[𓉘❀𓉝]({channel_link}) 𝗖𝗵𝗲𝗰𝗸𝘀: `{user_data['total_checks']}`
[𓉘❀𓉝]({channel_link}) 𝗦𝘁𝗮𝘁𝘂𝘀: {status}"""
                    
                    print(f"[DEBUG] Profile message generated for user {user_id}")
                    print(f"[DEBUG] Message length: {len(profile_msg_plain)} bytes")
                except Exception as e:
                    print(f"[ERROR] Failed to generate profile message: {e}")
                    import traceback
                    traceback.print_exc()
                    bot.answer_callback_query(call.id, "⚠️ 𝗔𝗻 𝗲𝗿𝗿𝗼𝗿 𝗼𝗰𝗰𝘂𝗿𝗿𝗲𝗱.")
                    return
                
                try:
                    bot.edit_message_caption(
                        profile_msg_plain,
                        call.message.chat.id,
                        call.message.message_id,
                        parse_mode='Markdown',
                        reply_markup=types.InlineKeyboardMarkup(row_width=2).add(
                            types.InlineKeyboardButton('📢 Channel', url=f"https://t.me/{channel_username}"),
                            types.InlineKeyboardButton('👑 Owner', url=owner_url)
                        ).add(
                            types.InlineKeyboardButton('🔙 BACK', callback_data='back_to_start')
                        )
                    )
                    print(f"[DEBUG] Profile caption edited successfully")
                except Exception as e:
                    print(f"[ERROR] Failed to edit caption: {e}")
                    import traceback
                    traceback.print_exc()
                    bot.answer_callback_query(call.id, "⚠️ 𝗔𝗻 𝗲𝗿𝗿𝗼𝗿 𝗼𝗰𝗰𝘂𝗿𝗿𝗲𝗱.")
                    return
                bot.answer_callback_query(call.id)
            
            elif call.data == 'commands':
                if not user_manager.is_registered(user_id):
                    bot.answer_callback_query(call.id, "⚠️ 𝗣𝗹𝗲𝗮𝘀𝗲 𝗿𝗲𝗴𝗶𝘀𝘁𝗲𝗿 𝗳𝗶𝗿𝘀𝘁!")
                    return
                
                channel_link = f"https://t.me/{channel_username}"
                
                commands_msg = f"""[𓉘❀𓉝]({channel_link}) 𝗣𝗮𝗴𝗲 1

━━━━━━━━━━━━━
[𓉘❀𓉝]({channel_link}) Gateway CC Killer ($0.00)
[𓉘❀𓉝]({channel_link}) Use ➛ `/kill cc|mm|yy|cvv`
[𓉘❀𓉝]({channel_link}) Status ➛ ONLINE ✅
[𓉘❀𓉝]({channel_link}) Type ➛ Free
━━━━━━━━━━━━━
[𓉘❀𓉝]({channel_link}) Gateway Braintree Auth ($1.00)
[𓉘❀𓉝]({channel_link}) Use ➛ `/chk cc|mm|yy|cvv`
[𓉘❀𓉝]({channel_link}) Status ➛ ONLINE ✅
[𓉘❀𓉝]({channel_link}) Type ➛ Free
━━━━━━━━━━━━━"""
                
                markup = types.InlineKeyboardMarkup(row_width=2)
                markup.add(
                    types.InlineKeyboardButton('📢 Channel', url=channel_link),
                    types.InlineKeyboardButton('👑 Owner', url=owner_url)
                )
                markup.add(types.InlineKeyboardButton('🔙 BACK', callback_data='back_to_start'))
                
                try:
                    bot.edit_message_caption(
                        commands_msg,
                        call.message.chat.id,
                        call.message.message_id,
                        parse_mode='Markdown',
                        reply_markup=markup
                    )
                except Exception as e:
                    print(f"[ERROR] Failed to show commands: {e}")
                    import traceback
                    traceback.print_exc()
                
                bot.answer_callback_query(call.id, "⚡ 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀 𝗺𝗲𝗻𝘂")
            
            elif call.data == 'gates':
                channel_link = f"https://t.me/{channel_username}"
                gates_msg = f"""[𓉘❀𓉝]({channel_link}) 𝗚𝗮𝘁𝗲𝘀

[𓉘❀𓉝]({channel_link}) 𝗖𝗼𝗺𝗶𝗻𝗴 𝗦𝗼𝗼𝗻..."""
                
                try:
                    bot.edit_message_caption(
                        gates_msg,
                        call.message.chat.id,
                        call.message.message_id,
                        parse_mode='Markdown',
                        reply_markup=types.InlineKeyboardMarkup().add(
                            types.InlineKeyboardButton('🔙 BACK', callback_data='back_to_start')
                        )
                    )
                except:
                    try:
                        bot.edit_message_text(
                            gates_msg,
                            call.message.chat.id,
                            call.message.message_id,
                            parse_mode='Markdown',
                            reply_markup=types.InlineKeyboardMarkup().add(
                                types.InlineKeyboardButton('🔙 BACK', callback_data='back_to_start')
                            ),
                            disable_web_page_preview=True
                        )
                    except Exception as e:
                        bot.answer_callback_query(call.id, "⚠️ 𝗔𝗻 𝗲𝗿𝗿𝗼𝗿 𝗼𝗰𝗰𝘂𝗿𝗿𝗲𝗱.")
                        return
                bot.answer_callback_query(call.id)
            
            elif call.data == 'exit':
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.answer_callback_query(call.id, "👋 𝗚𝗼𝗼𝗱𝗯𝘆𝗲!")
            
            elif call.data == 'back_to_start':
                is_registered = user_manager.is_registered(user_id)
                first_name = str(call.from_user.first_name).encode('utf-16', 'surrogatepass').decode('utf-16', 'ignore') if call.from_user.first_name else 'User'
                
                welcome_msg = format_welcome_message(first_name, is_registered, channel_username)
                markup = create_start_keyboard(is_registered)
                
                try:
                    bot.edit_message_caption(
                        welcome_msg,
                        call.message.chat.id,
                        call.message.message_id,
                        parse_mode='Markdown',
                        reply_markup=markup
                    )
                except:
                    try:
                        bot.edit_message_text(
                            welcome_msg,
                            call.message.chat.id,
                            call.message.message_id,
                            parse_mode='Markdown',
                            reply_markup=markup,
                            disable_web_page_preview=True
                        )
                    except Exception as e:
                        bot.answer_callback_query(call.id, "⚠️ 𝗔𝗻 𝗲𝗿𝗿𝗼𝗿 𝗼𝗰𝗰𝘂𝗿𝗿𝗲𝗱.")
                        return
                bot.answer_callback_query(call.id)
        
        except Exception as e:
            print(f"[ERROR] Callback handler error: {e}")
            import traceback
            traceback.print_exc()
            try:
                bot.answer_callback_query(call.id, "⚠️ 𝗔𝗻 𝗲𝗿𝗿𝗼𝗿 𝗼𝗰𝗰𝘂𝗿𝗿𝗲𝗱.")
            except:
                pass