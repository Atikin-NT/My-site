import telebot

print("start")
token = '1668670487:AAFY33GR81tRtjQwvOWpzumndBpQemI0fxA'

bot = telebot.TeleBot(token)
photo = open('test.jpeg', 'rb')
mess_to_photo = """ 
<strong>6 конференций DevOps 2021</strong>

Новый год, новые начинания и новые конференции. 
Это снова то время года, когда участники конференции рассматривают различные площадки для участия. 
Чтобы сделать ваш обзор и исследование легким, вот пять лучших виртуальных конференций DevOps, которые вы можете посетить бесплатно. 
Ну, мы говорим только о виртуальных конференциях, поскольку они, похоже, работают хорошо и требуют меньше головной боли как для организаторов, так и для участников.

Читать делее на <a href="http://niktech.site/">сайте</a>
"""

@bot.message_handler(commands=['start'])
def start_message(message):
    #bot.send_message(message.chat.id, mess_to_photo, parse_mode="HTML")
    bot.send_photo(message.chat.id, photo, caption=mess_to_photo, parse_mode="HTML")

bot.polling()