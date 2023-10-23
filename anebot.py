import sqlite3
import telebot
from telebot import types
from settings import TOKEN

bot = telebot.TeleBot(TOKEN)


def create_inline_keyboard():
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Давай ещё', callback_data='button1')
    markup.add(button1)
    return markup


def get_random_anek():
    conn = sqlite3.connect('aneki.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, text FROM aneki ORDER BY RANDOM() LIMIT 1")
    anek = cursor.fetchone()
    conn.close()
    return anek if anek else "Извините, но у меня нет шуток сегодня."


def create_database_users():
    create_table_query = '''
           CREATE TABLE IF NOT EXISTS users (
               user_id INTEGER UNIQUE,
               anek_id INTEGER
           )
    '''
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()


def insert_userid_to_usersdb(user_id: int):
    insert_data_query = '''
            INSERT OR IGNORE INTO users (user_id)
            VALUES (?)    
    '''
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(insert_data_query, (user_id,))
    conn.commit()
    conn.close()


def insert_anekid_to_usersdb(user_id: int, anek_id: int):
    insert_data_query = '''
        UPDATE users
        SET anek_id =
            CASE
                WHEN anek_id IS NULL OR anek_id = '' THEN ?
                ELSE anek_id || ', ' || ?
            END
        WHERE user_id = ? 
    '''
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(insert_data_query, (anek_id, anek_id, user_id))
    conn.commit()
    conn.close()


def get_anek_ids_from_usersbd(user_id):
    get_data_query = f'SELECT anek_id FROM users WHERE user_id = {user_id}'
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(get_data_query, (user_id,))
    result = cursor.fetchone()
    conn.close()
    anek_ids = result[0].split(', ')
    return anek_ids


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = create_inline_keyboard()
    anek = get_random_anek()
    anek_id = anek[0]
    anek_text = anek[1]
    user_id = message.chat.id
    create_database_users()
    insert_userid_to_usersdb(user_id)
    insert_anekid_to_usersdb(user_id=user_id, anek_id=anek_id)
    bot.send_message(message.chat.id, anek_text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'button1':
        markup = create_inline_keyboard()
        anek = get_random_anek()
        anek_id = anek[0]
        anek_text = anek[1]
        user_id = call.message.chat.id
        insert_anekid_to_usersdb(user_id=user_id, anek_id=anek_id)
        bot.send_message(call.message.chat.id, anek_text, reply_markup=markup)


bot.infinity_polling()

if __name__ == '__main__':
    bot.polling(none_stop=True)
