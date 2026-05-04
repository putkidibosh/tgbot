import requests
import os
import time
from urllib.parse import quote

# ⚔️ API Configuration
API_URL = "https://www.noobs-apis.run.place"

config = {
    "name": "sing",
    "description": "Search and download MP3 songs ⚔️",
    "usage": "/sing <song name>"
}

# ⚔️ ইন-মেমোরি স্টোরেজ (সার্চ রেজাল্ট সাময়িকভাবে রাখার জন্য)
search_results = {}

def handle(bot, message, args):
    if not args:
        return bot.reply_to(message, "⚔️ 𝐏𝐥𝐞𝐚𝐬𝐞 𝐭𝐲𝐩𝐞 𝐚 𝐬𝐨𝐧𝐠 𝐧𝐚𝐦𝐞! (𝐄𝐱: /sing suno sajna)")

    query = " ".join(args)
    user_id = message.from_user.id
    
    # ⚔️ Loading message
    sent_msg = bot.reply_to(message, "⏳ ⚔️ Searching for your song...")

    try:
        # ⚔️ Searching on YouTube via API
        search_api = f"{API_URL}/nazrul/youtube?type=s&query={quote(query)}"
        res = requests.get(search_api).json()
        videos = res.get('results', {}).get('data', [])

        if not videos:
            return bot.edit_message_text("⚔️ 𝐍𝐨 𝐫𝐞𝐬𝐮𝐥𝐭𝐬 𝐟𝐨𝐮𝐧𝐝!", message.chat.id, sent_msg.message_id)

        # ⚔️ রেজাল্ট লিস্ট তৈরি করা
        txt = "⚔️ 𝐒𝐞𝐚𝐫𝐜𝐡 𝐑𝐞𝐬𝐮𝐥𝐭𝐬 ⚔️\n━━━━━━━━━━━━━━━\n"
        temp_data = []

        for i, v in enumerate(videos[:10]):
            txt += f"{i + 1}. {v['title']}\n🎬 𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧: {v.get('duration', 'N/A')}\n\n"
            temp_data.append(v)

        txt += "━━━━━━━━━━━━━━━\n⚔️ 𝐑𝐞𝐩𝐥𝐲 𝐰𝐢𝐭𝐡 𝐭𝐡𝐞 𝐧𝐮𝐦𝐛𝐞𝐫 (𝟏-𝟏𝟎) 𝐭𝐨 𝐠𝐞𝐭 𝐌𝐏𝟑."
        
        # ⚔️ সেভ করা যাতে ইউজার রিপ্লাই দিলে বোট বুঝতে পারে
        search_results[user_id] = temp_data
        
        # ⚔️ মেসেজ এডিট করে লিস্ট দেখানো
        bot.edit_message_text(txt, message.chat.id, sent_msg.message_id)

        # ⚔️ পরবর্তী মেসেজের জন্য ওয়েট করা (রিপ্লাই হ্যান্ডেলার)
        bot.register_next_step_handler(sent_msg, lambda m: process_selection(bot, m, user_id))

    except Exception as e:
        bot.edit_message_text(f"⚠️ 𝐒𝐲𝐬𝐭𝐞𝐦 𝐄𝐫𝐫𝐨𝐫: {str(e)}", message.chat.id, sent_msg.message_id)

def process_selection(bot, message, user_id):
    # ⚔️ ইউজার চেক
    if message.from_user.id != user_id:
        return

    text = message.text.strip()
    if not text.isdigit():
        return bot.reply_to(message, "⚔️ Invalid selection. Please use a number.")

    idx = int(text) - 1
    if user_id not in search_results or idx < 0 or idx >= len(search_results[user_id]):
        return bot.reply_to(message, "⚔️ Selection out of range or session expired.")

    selected_video = search_results[user_id][idx]
    video_id = selected_video['id']
    video_title = selected_video['title']
    
    # ⚔️ ডিরেক্ট ইউটিউব লিংক তৈরি
    yt_url = f"https://www.youtube.com/watch?v={video_id}"
    
    sent_msg = bot.reply_to(message, f"📥 ⚔️ Downloading: {video_title}...")

    try:
        # ⚔️ MP3 Download API Call
        dl_api = f"{API_URL}/nazrul/youtube?type=mp3&url={quote(yt_url)}"
        dl_res = requests.get(dl_api).json()
        download_url = dl_res.get('download_url')

        if not download_url:
            return bot.edit_message_text("⚔️ Failed to get download link.", message.chat.id, sent_msg.message_id)

        # ⚔️ ফাইল পাথ এবং ডাউনলোড
        file_path = f"cache/song_{int(time.time())}.mp3"
        if not os.path.exists("cache"): os.makedirs("cache")
        
        response = requests.get(download_url).content
        with open(file_path, "wb") as f:
            f.write(response)

        # ⚔️ অডিও পাঠানো
        with open(file_path, "rb") as audio:
            bot.send_audio(
                message.chat.id, 
                audio, 
                title=video_title,
                caption=f"✅ ⚔️ 𝐒𝐨𝐧𝐠: {video_title}\n⚔️ 𝐒𝐲𝐬𝐭𝐞𝐦 𝐁𝐲: 𝐌𝐫.𝐊𝐢𝐧𝐠 🕊️💖",
                reply_to_message_id=message.message_id
            )

        # ⚔️ Cleanup
        bot.delete_message(message.chat.id, sent_msg.message_id)
        if os.path.exists(file_path): os.remove(file_path)
        
        # ⚔️ সেশন ক্লিয়ার
        del search_results[user_id]

    except Exception as e:
        bot.edit_message_text(f"⚠️ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐄𝐫𝐫𝐨𝐫: {str(e)}", message.chat.id, sent_msg.message_id)
        if 'file_path' in locals() and os.path.exists(file_path): os.remove(file_path)
            
