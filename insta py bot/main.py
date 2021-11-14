from instabot import Bot
import shutil

def insta_bot():
    try:
        shutil.rmtree('config')
    except FileNotFoundError: pass
    bot = Bot()
    bot.login(username="niktech_nt_site", password="niktech_top")
    bot.upload_photo("test.jpg",
                    caption ="Technical Scripter Event 2021")