import telebot
import requests
import json

API = ''
token = ''
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])

def start(message):
    bot.send_message(message.chat.id, 'Привет,😊 рад тебя видеть! Пожалуйста, укажи город, в котором нужно узнать погоду!')
    
@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        bot.reply_to(message, f'Погода сейчас:  {temp}')
        
        image = 'Sun_and_clouds.jpg' if temp > 5.0 else 'sun.png'
        file = open('./' + image, 'rb')
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to('Город указан неверно, повторите ввод.')
    
bot.polling(non_stop=True)