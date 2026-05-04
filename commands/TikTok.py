import requests
import os
import json
import random
import time
from urllib.parse import quote

# ⚔️ History Path setup
CACHE_DIR = "cache"
HISTORY_PATH = os.path.join(CACHE_DIR, "tikHistory.json")

# ⚔️ Ensure cache directory exists
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

config = {
    "name": "tik",
    "description": "Download TikTok video by search ⚔️",
    "usage": "/tik <video/song name>"
}

def get_history():
    if not os.path.exists(HISTORY_PATH):
        return []
    try:
        with open(HISTORY_PATH, "r") as f:
            return json.load(f)
    except:
        return []

def save_history(history):
    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f)

def handle(bot, message, args):
    if not args:
        return bot.reply_to(message, "⚔️ 𝐏𝐥𝐞𝐚𝐬𝐞 𝐭𝐲𝐩𝐞 𝐚 𝐯𝐢𝐝𝐞𝐨 𝐨𝐫 𝐬𝐨𝐧𝐠 𝐧𝐚𝐦𝐞!")

    query = " ".join(args)
    bot.send_chat_action(message.chat.id, 'upload_video')
    
    # ⚔️ Loading message
    sent_msg = bot.reply_to(message, "⏳ ⚔️ Searching on TikTok...")
    file_path = os.path.join(CACHE_DIR, f"tik_{int(time.time())}.mp4")

    try:
        # ⚔️ TikWM API Call
        search_url = f"https://www.tikwm.com/api/feed/search?keywords={quote(query)}"
        res = requests.get(search_url).json()
        video_list = res.get('data', {}).get('videos', [])

        if not video_list:
            return bot.edit_message_text("⚔️ 𝐍𝐨 𝐯𝐢𝐝𝐞𝐨 𝐟𝐨𝐮𝐧𝐝!", message.chat.id, sent_msg.message_id)

        history = get_history()
        
        # ⚔️ Filtering seen videos
        filtered_videos = [v for v in video_list if v.get('video_id') not in history]

        # ⚔️ Reset history if all videos are seen
        if not filtered_videos:
            filtered_videos = video_list
            video_ids = [v.get('video_id') for v in video_list]
            history = [vid for vid in history if vid not in video_ids]

        # ⚔️ Pick a random video from top 15
        video_data = random.choice(filtered_videos[:15])
        
        # ⚔️ Save to history (Limit to 150)
        history.append(video_data.get('video_id'))
        if len(history) > 150:
            history.pop(0)
        save_history(history)

        video_url = video_data.get('play')

        if video_url:
            # ⚔️ Download
            response = requests.get(video_url, timeout=20).content
            with open(file_path, 'wb') as f:
                f.write(response)

            # ⚔️ Send Video
            with open(file_path, 'rb') as video_file:
                bot.send_video(
                    message.chat.id, 
                    video_file, 
                    caption=f"✅ ⚔️ 𝐇𝐞𝐫𝐞 𝐢𝐬 𝐲𝐨𝐮𝐫 𝐯𝐢𝐝𝐞𝐨 🕊️💖\n⚔️ 𝐒𝐲𝐬𝐭𝐞𝐦 𝐁𝐲: 𝐌𝐫.𝐊𝐢𝐧𝐠",
                    reply_to_message_id=message.message_id
                )
            bot.delete_message(message.chat.id, sent_msg.message_id)
        else:
            bot.edit_message_text("⚔️ Video link not found.", message.chat.id, sent_msg.message_id)

    except Exception as e:
        print(f"Error: {e}")
        bot.edit_message_text("⚔️ 𝐒𝐲𝐬𝐭𝐞𝐦 𝐁𝐮𝐬𝐲! 𝐓𝐫𝐲 𝐚𝐠𝐚𝐢𝐧.", message.chat.id, sent_msg.message_id)
    
    finally:
        # ⚔️ Cleanup cache
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
                
