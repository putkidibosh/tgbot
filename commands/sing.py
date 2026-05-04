import requests
import os
import time
from urllib.parse import quote

# ⚔️ Command Configuration
config = {
    "name": "sing",
    "description": "Download MP3 from YouTube ⚔️",
    "usage": "/sing <song name>"
}

def handle(bot, message, args):
    if not args:
        return bot.reply_to(message, "⚔️ Please provide a song name or YouTube link!")

    query = " ".join(args)
    # ⏳ Processing message
    sent_msg = bot.reply_to(message, "⏳ ⚔️ Searching for your song...")
    api_base = "https://www.noobs-apis.run.place"

    try:
        # ⚔️ Step 1: Search for the video
        search_api = f"{api_base}/nazrul/youtube?type=s&query={quote(query)}"
        search_data = requests.get(search_api).json()
        
        results = search_data.get('results', {}).get('data', [])
        if not results:
            return bot.edit_message_text("⚔️ No results found on YouTube.", message.chat.id, sent_msg.message_id)

        video = results[0]
        video_id = video['id']
        video_title = video['title']
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        # ⚔️ Step 2: Get the MP3 download link
        download_api = f"{api_base}/nazrul/youtube?type=mp3&url={quote(video_url)}"
        dl_data = requests.get(download_api).json()
        audio_link = dl_data.get('download_url')

        if not audio_url:
            return bot.edit_message_text("⚔️ Download link not found! Try again later.", message.chat.id, sent_msg.message_id)

        # ⚔️ Step 3: Download the file to local storage
        file_path = f"song_{int(time.time())}.mp3"
        response = requests.get(audio_link)
        
        with open(file_path, "wb") as f:
            f.write(response.content)

        # ⚔️ Step 4: Send the Audio to Telegram
        with open(file_path, "rb") as audio_file:
            bot.send_audio(
                message.chat.id, 
                audio_file, 
                caption=f"✅ ⚔️ Title: {video_title}\n⚔️ System By: Mr.King",
                reply_to_message_id=message.message_id
            )

        # ⚔️ Cleanup: Delete temp file and processing message
        bot.delete_message(message.chat.id, sent_msg.message_id)
        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception as e:
        error_msg = f"⚔️ Error: {str(e)}"
        bot.edit_message_text(error_msg, message.chat.id, sent_msg.message_id)
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
