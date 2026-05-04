import requests
import os
import random
import time

# ⚔️ Memory to track seen videos
if 'anime_video_memory' not in globals():
    global anime_video_memory
    anime_video_memory = set()

config = {
    "name": "anime",
    "description": "Get a random anime 4K video ⚔️"
}

def handle(bot, message, args):
    # ⚔️ Telegram Chat IDs (Replace with your actual Telegram ID)
    boss_id = 123456789  # আপনার টেলিগ্রাম আইডি এখানে দিন
    cost = 1000
    sender_id = message.from_user.id

    # ⚔️ Loading message
    sent_msg = bot.reply_to(message, "🎬 𝐋𝐨𝐚𝐝𝐢𝐧𝐠 𝐫𝐚𝐧𝐝𝐨𝐦 𝐚𝐧𝐢𝐦𝐞 𝐯𝐢𝐝𝐞𝐨... 𝐏𝐥𝐞𝐚𝐬𝐞 𝐰𝐚𝐢𝐭 𝐛𝐛𝐲 🕊️💖")

    try:
        # ⚔️ Anime Tags for high quality edits
        anime_tags = [
            "anime attitude edit 4k",
            "anime sigma male edit",
            "badass anime moments 4k",
            "anime phonk edit 4k",
            "anime 4k 60fps attitude",
            "anime savage moments 4k"
        ]

        random_tag = random.choice(anime_tags)
        
        # ⚔️ Fetching from TikWM API
        search_url = f"https://www.tikwm.com/api/feed/search?keywords={random_tag}"
        res = requests.get(search_url).json()
        videos = res.get('data', {}).get('videos', [])

        if not videos:
            return bot.edit_message_text("⚔️ No video found! Try again boss.", message.chat.id, sent_msg.message_id)

        # ⚔️ Video Selection Logic
        global anime_video_memory
        selected = next((v for v in videos if v['video_id'] not in anime_video_memory), None)
        
        if not selected:
            anime_video_memory.clear()
            selected = random.choice(videos)
        
        anime_video_memory.add(selected['video_id'])
        video_play_url = selected['play']

        # ⚔️ Temporary file path
        file_path = f"anime_{int(time.time())}.mp4"
        
        # ⚔️ Downloading video
        video_data = requests.get(video_play_url).content
        with open(file_path, "wb") as f:
            f.write(video_data)

        # ⚔️ Sending Video
        with open(file_path, "rb") as video_file:
            bot.send_video(
                message.chat.id, 
                video_file, 
                caption=f"⚔️ 𝐇𝐞𝐫𝐞 𝐢𝐬 𝐲𝐨𝐮𝐫 𝐚𝐧𝐢𝐦𝐞 𝐯𝐢𝐝𝐞𝐨 ⚔️\n\n🦭 𝐒𝐲𝐬𝐭𝐞𝐦 𝐁𝐲: 𝐌𝐫.𝐊𝐢𝐧𝐠 🕊️💖",
                reply_to_message_id=message.message_id
            )

        # ⚔️ Cleanup
        bot.delete_message(message.chat.id, sent_msg.message_id)
        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception as e:
        bot.edit_message_text(f"⚠️ 𝐒𝐲𝐬𝐭𝐞𝐦 𝐄𝐫𝐫𝐨𝐫: {str(e)}", message.chat.id, sent_msg.message_id)
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
