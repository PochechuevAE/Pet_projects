import telebot
from telebot import types
# import webbrowser

bot = telebot.TeleBot('6986054447:AAFuVoogeGq6Fu8ZqKwwCKsewQWfCtw5NfY')

@bot.message_handler(commands=['start']) #  Добавляем стартовые кнопки
def start(message):
    markup = types.ReplyKeyboardMarkup() 
    btn1 = types.KeyboardButton('info')
    btn2 = types.KeyboardButton('Привет')
    btn3 = types.KeyboardButton('id')
    markup.row(btn1) # добавляем саму кнопку в 1 ряд
    markup.row(btn2, btn3) # добавляем саму кнопки во 2 ряд
    bot.send_message(message.chat.id, 'Добро пожаловать 😍', reply_markup=markup)
    # Если вместо сообщения отправлять картинку:
    # file = open('./photo.jpeg', 'rb') # Если фото лежит в этой же папке, формат открытия rb = открытие на чтение
    # bot.send_photo(message.chat.id, file, reply_markup=markup) # клавиши добавляются по желанию
    # Так же и аудио фаил метод аналогичен bot.send_audio(message.chat.id, file, reply_markup=markup) только file меняется
    # С видео аналогично
    
    
    #bot.register_next_step_handler(message, on_click) # Обработка нажатия на кнопку чтобы работала только 1 раз кнопка

# def on_click(message): # Срабатывает один раз, вне зависимости от того, что пользователь ввёл
#     if message.text == 'info':
#         bot.send_message(message.chat.id, 'Спроси у гугла')

# @bot.message_handler(commands=['site', 'website', 'сайт'])
# def site(message):
#     webbrowser.open('https://hd.kinopoisk.ru')

markup = types.InlineKeyboardMarkup() # Создаем объект и импортируем в него из types вот это InlineKeyboardMarkup
btn1 = types.InlineKeyboardButton('Перейти на сайт', url= 'http://google.com')
btn2 = types.InlineKeyboardButton('Удалить фото', callback_data='delete')
btn3 = types.InlineKeyboardButton('Изменить текст', callback_data='edit')
markup.row(btn1) # добавляем саму кнопку в 1 ряд
markup.row(btn2, btn3) # добавляем саму кнопки во 2 ряд



@bot.callback_query_handler(func=lambda callback: True) # Если параметр пустой, то тру
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit Message', callback.message.chat.id, callback.message.message_id - 1)
    
@bot.message_handler(commands=['start']) # Это декоратор функции При нажатии на start выводит сообщение
def start_message(message):
	bot.send_message(message.chat.id, f'Добро пожаловать, {message.from_user.first_name} {message.from_user.last_name}')
 
@bot.message_handler(commands=['info']) # Это декоратор функции При нажатии на info выводит сообщение
def start_message(message):
	bot.send_message(message.chat.id, "Спроси у гугла") # параметр reply_markup=markup добавил
                                                                             # кнопку к сообщению

@bot.message_handler(content_types=['photo']) # Срабатывает тогда, когда бот получает фото
def get_photo(message):
    bot.reply_to(message, f"Какое красивое фото", reply_markup=markup)

@bot.message_handler() #Этот декоратор обрабатывает введённые данные от пользователя
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, привет, {message.from_user.first_name} {message.from_user.last_name}')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'Ваш Id: {message.from_user.id}') # Метод выводит ответ на предыдущее сообщение

bot.polling(non_stop=True) # Делает программу работающей постоянно