from telebot import types

def create_start_keyboard(is_registered):
    markup = types.InlineKeyboardMarkup(row_width=2)
    if not is_registered:
        register_btn = types.InlineKeyboardButton('✨ REGISTER', callback_data='register')
        markup.add(register_btn)
    else:
        profile_btn = types.InlineKeyboardButton('👤 PROFILE', callback_data='profile')
        exit_btn = types.InlineKeyboardButton('❌ EXIT', callback_data='exit')
        commands_btn = types.InlineKeyboardButton('⚡ COMMANDS', callback_data='commands')
        markup.row(profile_btn, exit_btn)
        markup.add(commands_btn)
    
    return markup

def create_gates_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    gates_btn = types.InlineKeyboardButton('🔐 GATES', callback_data='gates')
    markup.add(gates_btn)
    return markup
