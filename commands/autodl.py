import requests
import os
import time
import re

# ⚔️ Base URL fetching function
def get_base_url():
    try:
        res = requests.get("https://raw.githubusercontent.com/mahmudx7/HINATA/main/baseApiUrl.json", timeout=10)
        return res.json().get("mahmud")
    except:
        return "https://mahmud-global-apis.onrender.com"

config = {
    "name": "autodl",
    "description": "Auto download videos from links ⚔️",
    "usage": "Just paste a video link"
}

def handle(bot, message, args):
    # This command normally triggers via link detection in main.py engine
    # But we keep this handle function for direct call compatibility
    if not args:
        return
    process_link(bot, message, args[0])

def process_link(bot, message, link):
    # ⚔️ Site detection logic
    platform = "𝚄𝚗𝚔𝚗𝚘𝚠𝚗"
    if "facebook.com" in link or "fb.watch" in link:
        platform = "𝐅𝐚𝐜𝐞𝐛𝐨𝐨𝐤"
    elif "instagram.com" in link:
        platform = "𝐈𝐧𝐬𝐭𝐚𝐠𝐫𝐚𝐦"
    elif "tiktok.com" in link:
        platform = "𝐓𝐢𝐤𝐓𝐨𝐤"
    elif "youtu.be" in link or "youtube.com" in link:
        platform = "𝐘𝐨𝐮𝐓𝐮𝐛𝐞"
    elif "x.com" in link or "twitter.com" in link:
        platform = "𝐗 (𝐓𝐰𝐢𝐭𝐭𝐞𝐫)"
    else:
        return

    # ⚔️ Cache setup
    if not os.path.exists("cache"):
        os.makedirs("cache")
        
    file_path = f"cache/autodl_{int(time.time())}.mp4"

    try:
        base = get_base_url()
        api_url = f"{base}/api/download/video?link={link}"
        
        # ⚔️ Downloading video
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        }
        
        response = requests.get(api_url, headers=headers, stream=True, timeout=60)
        
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            if os.path.getsize(file_path) < 1000:
                return

            # ⚔️ Sending video
            caption_text = (
                f"❐ 𝐏𝐥𝐚𝐭𝐟𝐨𝐫𝐦: {platform}\n"
                "━━━━━━━━━━━━━━\n"
                "🎬 𝗠𝗿.𝗞𝗶𝗻𝗴 ⚔️"
            )
            
            with open(file_path, 'rb') as video_file:
                bot.send_video(
                    message.chat.id, 
                    video_file, 
                    caption=caption_text,
                    reply_to_message_id=message.message_id
                )
            
    except Exception as e:
        print(f"AutoDL Error: {str(e)}")
        
    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass

# ⚔️ Integration Tip: 
# To make this work automatically, add this to your main.py:
# @bot.message_handler(func=lambda m: re.search(r'https?://\S+', m.text) and not m.text.startswith('/'))
# def auto_dl_trigger(message):
#     link = re.search(r'https?://\S+', message.text).group(0)
#     process_link(bot, message, link)
