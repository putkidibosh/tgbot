import requests
import os
import random
import time
from urllib.parse import quote

# ⚔️ Global state (In-memory)
if 'bhojpuri_users' not in globals():
    global bhojpuri_users, bhojpuri_status
    bhojpuri_users = set() # এখানে ইউজার আইডিগুলো জমা থাকবে
    bhojpuri_status = True

config = {
    "name": "bhojpuri",
    "description": "Get viral or search specific videos ⚔️"
}

def handle(bot, message, args):
    global bhojpuri_users, bhojpuri_status
    
    # ⚔️ Admin Username (Your Telegram Username)
    boss_username = "mr_King1430" 
    sender_username = message.from_user.username
    sender_id = message.from_user.id

    # ⚔️ Admin Commands (Only for mr_King1430)
    if args and sender_username == boss_username:
        if args[0] == "add" and message.reply_to_message:
            target_id = message.reply_to_message.from_user.id
            bhojpuri_users.add(target_id)
            return bot.reply_to(message, "✅ 𝐔𝐬𝐞𝐫 𝐚𝐝𝐝𝐞𝐝 𝐭𝐨 𝐭𝐡𝐞 𝐫𝐞𝐬𝐭𝐫𝐢𝐜𝐭𝐞𝐝 𝐥𝐢𝐬𝐭! ⚔️")
        
        if args[0] == "on":
            bhojpuri_status = True
            return bot.reply_to(message, "✅ 𝐂𝐨𝐦𝐦𝐚𝐧𝐝 𝐭𝐮𝐫𝐧𝐞𝐝 𝐎𝐍! ⚔️")
        
        if args[0] == "off":
            bhojpuri_status = False
            return bot.reply_to(message, "❌ 𝐂𝐨𝐦𝐦𝐚𝐧𝐝 𝐭𝐮𝐫𝐧𝐞𝐝 𝐎𝐅𝐅! ⚔️")

    # ⚔️ Access Check
    if sender_username != boss_username and sender_id not in bhojpuri_users:
        return # লিস্টে না থাকলে বোট রিপ্লাই দিবে না
    
    if not bhojpuri_status:
        return

    query = " ".join(args)
    random_terms = [
        "bhojpuri hot dance reels", "russian girl viral reels 4k", "bangla dj song dance video", 
        "bangla girl viral dance tiktok", "suno sajna re", "nyxlu queen", "nyxly edit", 
        "Russian queen", "black pink 4k", "black pink hot", "Bangla hot girls", 
        "hot girls", "hot nagin dance", "Indian hot girls", "trending hot reels 2026"
    ]

    current_search = query if query else random.choice(random_terms)
    sent_msg = bot.reply_to(message, "⏳ ⚔️ Searching for content...")

    try:
        # ⚔️ Fetching from TikWM API
        videos = []
        attempts = 0
        while not videos and attempts < 5:
            search_url = f"https://www.tikwm.com/api/feed/search?keywords={quote(current_search)}"
            res = requests.get(search_url).json()
            videos = res.get('data', {}).get('videos', [])
            if not videos:
                current_search = random.choice(random_terms)
                attempts += 1

        if not videos:
            return bot.edit_message_text("⚠️ 𝐒𝐞𝐫𝐯𝐞𝐫 𝐁𝐮𝐬𝐲! ⚔️", message.chat.id, sent_msg.message_id)

        selected_video = random.choice(videos)
        video_url = selected_video['play']
        file_path = f"bj_{int(time.time())}.mp4"

        # ⚔️ Download & Send
        video_data = requests.get(video_url).content
        with open(file_path, "wb") as f:
            f.write(video_data)

        with open(file_path, "rb") as video_file:
            bot.send_video(
                message.chat.id, 
                video_file, 
                caption=f"⚔️ 𝐑𝐞𝐬𝐮𝐥𝐭 𝐟𝐨𝐫: {current_search} ⚔️\n\n🦭 𝐒𝐲𝐬𝐭𝐞𝐦 𝐁𝐲: 𝐌𝐫.𝐊𝐢𝐧𝐠 🕊️💖",
                reply_to_message_id=message.message_id
            )

        # ⚔️ Cleanup
        bot.delete_message(message.chat.id, sent_msg.message_id)
        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception as e:
        bot.edit_message_text(f"⚠️ 𝐄𝐫𝐫𝐨𝐫: {str(e)} ⚔️", message.chat.id, sent_msg.message_id)
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
