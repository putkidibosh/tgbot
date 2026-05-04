import telebot
import os
import importlib

# ⚔️ আপনার বোট টোকেনটি এখানে দিন
TOKEN = "YOUR_BOT_TOKEN_HERE"
bot = telebot.TeleBot(TOKEN)

def load_commands():
    if not os.path.exists("commands"):
        os.makedirs("commands")
    
    for filename in os.listdir("commands"):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"commands.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, 'config') and hasattr(module, 'handle'):
                    cmd_name = module.config["name"]
                    
                    # ⚔️ কমান্ড রেজিস্টার
                    @bot.message_handler(commands=[cmd_name])
                    def wrapper(message, m=module):
                        args = message.text.split()[1:]
                        m.handle(bot, message, args)
                    
                    print(f"⚔️ Loaded: {cmd_name}")
            except Exception as e:
                print(f"⚔️ Failed to load {filename}: {e}")

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "⚔️ Chillup Bot Started!\nWelcome Mr.King")

if __name__ == "__main__":
    load_commands()
    print("⚔️ TgBot is Online!")
    bot.polling(none_stop=True)
    
