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
    cursor.execute("SELECT text FROM aneki ORDER BY RANDOM() LIMIT 1")
    joke = cursor.fetchone()
    conn.close()
    return joke[0] if joke else "Извините, но у меня нет шуток сегодня."


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = create_inline_keyboard()
    anek = get_random_anek()
    bot.send_message(message.chat.id, anek, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'button1':
        markup = create_inline_keyboard()
        anek = get_random_anek()
        bot.send_message(call.message.chat.id, anek, reply_markup=markup)


bot.infinity_polling()

if __name__ == '__main__':
    bot.polling(none_stop=True)
