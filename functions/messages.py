def format_welcome_message(first_name, is_registered, channel_username):
    channel_link = f"https://t.me/{channel_username}"
    
    if is_registered:
        message = f"""[𓉘❀𓉝]({channel_link}) 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝗕𝗮𝗰𝗸!

[𓉘❀𓉝]({channel_link}) 𝗛𝗲𝗹𝗹𝗼 **{first_name}**"""
    else:
        message = f"""[𓉘❀𓉝]({channel_link}) 𝗪𝗲𝗹𝗰𝗼𝗺𝗲!

[𓉘❀𓉝]({channel_link}) 𝗛𝗲𝗹𝗹𝗼 **{first_name}**

𝗣𝗹𝗲𝗮𝘀𝗲 𝗿𝗲𝗴𝗶𝘀𝘁𝗲𝗿 𝘁𝗼 𝗰𝗼𝗻𝘁𝗶𝗻𝘂𝗲"""
    
    return message
