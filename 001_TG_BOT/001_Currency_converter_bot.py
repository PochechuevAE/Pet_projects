import telebot
from telebot import types
from currency_converter import CurrencyConverter

Currency = CurrencyConverter()
token = ''
bot = telebot.TeleBot(token)
amaunt = 0

markup = types.InlineKeyboardMarkup(row_width = 2)
btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
btn4 = types.InlineKeyboardButton('Другое значение', callback_data='else')
markup.add(btn1,btn2,btn3,btn4)


@bot.callback_query_handler(func=lambda call: True)
def callback_message(callback):
    if callback.data != 'else':
        values = callback.data.upper().split('/')
        res = Currency.convert(amaunt, values[0], values[1])
        bot.send_message(callback.message.chat.id, f'Получается {round(res, 2)}. Можете заново вписать сумму.')
        bot.register_next_step_handler(callback.message, summa)
    if callback.data == 'else':
        bot.send_message(callback.message.chat.id, f'Введите пару значений через слэш')
        bot.register_next_step_handler(callback.message, my_currency)
         

@bot.message_handler(commands='start')
def start(message):
    bot.send_message(message.chat.id, 'Привет, введите сумму: ')
    bot.register_next_step_handler(message, summa)

def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = Currency.convert(amaunt, values[0], values[1])
        bot.send_message(message.chat.id, f'Получается {round(res, 2)}. Можете заново вписать сумму.')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, 'Что-то пошло не так. Впишите значение заново')
        bot.register_next_step_handler(message, my_currency)
        return
    
    
def summa(message):
    global amaunt
    try:
        amaunt = int(message.text.strip())
    except ValueError: 
        bot.send_message(message.chat.id, 'Неверный формат, повторите ввод!')
        bot.register_next_step_handler(message, summa)
        return
    if amaunt > 0:
        bot.send_message(message.chat.id, 'Выбирете пару для конвертации', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Число должно быть больше 0, повторите ввод!')
        bot.register_next_step_handler(message, summa)
        


bot.polling(non_stop=True)

