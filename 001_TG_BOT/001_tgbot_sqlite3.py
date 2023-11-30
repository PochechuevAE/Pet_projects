import telebot
from telebot import types
import sqlite3

#token = '6841705742:AAEHVPCszxkzSZE5Dq88RkLByTYlSJ0JDBc'
bot = telebot.TeleBot(token)
name = None

markup = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton('Список пользователей', callback_data='user_list')
btn2 = types.InlineKeyboardButton('Добавить пользвоателя', callback_data='add_new_user')
btn3 = types.InlineKeyboardButton('Редактировать пользователя', callback_data='edit')
btn4 = types.InlineKeyboardButton('Удалить пользователя', callback_data='delete')
markup.row(btn1, btn2)
markup.row(btn3, btn4)

@bot.message_handler(commands=['start']) #  Добавляем стартовые кнопки
def start(message):
    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()
    
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(50) NOT NULL,
                    pass VARCHAR(50)
                  )''')
    conn.commit()
    cur.close()
    conn.close()
    
    bot.send_message(message.chat.id, f'Добро пожаловать 😍 {message.from_user.first_name} {message.from_user.last_name},\nЗарегистрируйте имя пользователя:')
    bot.register_next_step_handler(message, user_name)   
    
def user_name(message):
    global name
    global count
    count = 1
    name = message.text.strip() #.strip - удаляет пробелы до и после текста
    
    bot.send_message(message.chat.id, f'''Введите его его пароль''')
    bot.register_next_step_handler(message, user_pass)

def user_pass(message):
    password = message.text.strip() 
    
    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()
    
    cur.execute('''INSERT INTO users (name, pass) VALUES ("%s", "%s")'''%(name, password))
    conn.commit()
    cur.close()
    conn.close()
    
    
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован!', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_message(callback):
    if callback.data == 'add_new_user':
        add_new_user(callback.message)
    elif callback.data == 'edit':
        edit_user(callback.message)
    elif callback.data == 'delete':
        delete_user(callback.message)
    elif callback.data == 'user_list':
        show_user_list(callback.message)

def add_new_user(message):
    bot.send_message(message.chat.id, 'Зарегистрируйте нового пользователя:')
    bot.register_next_step_handler(message, add_user_name)

def add_user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль пользователя:')
    bot.register_next_step_handler(message, add_user_pass)

def add_user_pass(message):
    password = message.text.strip()

    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()

    cur.execute('''INSERT INTO users (name, pass) VALUES (?, ?)''', (name, password))
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Пользователь успешно зарегистрирован!', reply_markup=markup)

def edit_user(message):
    bot.send_message(message.chat.id, 'Введите ID пользователя для редактирования:')
    bot.register_next_step_handler(message, edit_user_info)

def edit_user_info(message):
    user_id = message.text.strip()
    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user_info = cur.fetchone()
    cur.close()
    conn.close()

    if user_info:
        bot.send_message(message.chat.id, f'Текущее имя: {user_info[1]}, текущий пароль: {user_info[2]}')
        bot.send_message(message.chat.id, 'Введите новое имя:')
        bot.register_next_step_handler(message, lambda msg: edit_user_name(msg, user_id))
    else:
        bot.send_message(message.chat.id, 'Пользователь с таким ID не найден.', reply_markup=markup)

def edit_user_name(message, user_id):
    new_name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите новый пароль:')
    bot.register_next_step_handler(message, lambda msg: edit_user_pass(msg, user_id, new_name))

def edit_user_pass(message, user_id, new_name):
    new_pass = message.text.strip()

    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()

    cur.execute('UPDATE users SET name = ?, pass = ? WHERE id = ?', (new_name, new_pass, user_id))
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Пользователь успешно отредактирован!', reply_markup=markup)

def delete_user(message):
    bot.send_message(message.chat.id, 'Введите ID пользователя для удаления:')
    bot.register_next_step_handler(message, delete_user_info)

def delete_user_info(message):
    user_id = message.text.strip()
    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user_info = cur.fetchone()
    

    if user_info:
        bot.send_message(message.chat.id, f'Удалить пользователя с именем: {user_info[1]} и паролем: {user_info[2]}?')
        bot.send_message(message.chat.id, 'Да или Нет:')
        bot.register_next_step_handler(message, lambda msg: confirm_delete_user(msg, user_info))
    else:
        bot.send_message(message.chat.id, 'Пользователь с таким ID не найден.', reply_markup=markup)
    cur.close()
    conn.close()

def confirm_delete_user(message, user_info):
    confirm = message.text.strip().lower()
    if confirm == 'да':
        conn = sqlite3.connect('users.sql')
        cur = conn.cursor()

        cur.execute('DELETE FROM users WHERE id = ?', (user_info[0],))
        conn.commit()
        cur.close()
        conn.close()

        bot.send_message(message.chat.id, 'Пользователь успешно удален!', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Удаление отменено.', reply_markup=markup)


def show_user_list(message):
    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    all_users = cur.fetchall()
    info = ''
    for el in all_users:
        info += f'ID: {el[0]}, Имя: {el[1]}, Пароль: {el[2]}\n'

    cur.close()
    conn.close()

    bot.send_message(message.chat.id, info, reply_markup=markup)

          
bot.polling(non_stop=True) # Делает программу работающей постоянно