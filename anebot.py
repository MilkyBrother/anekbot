from telebot import TeleBot, types
from decouple import config
import database_api as db
from os import path

TOKEN = config('TOKEN')
bot = TeleBot(TOKEN)


def create_inline_keyboard() -> types.InlineKeyboardMarkup():
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Давай ещё', callback_data='button1')
    markup.add(button1)
    return markup


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = create_inline_keyboard()
    user_id = message.chat.id
    if not path.exists('users.db'):
        db.create_database_users()
    db.insert_userid_to_usersdb(user_id)
    anek_text = db.get_unique_anek(user_id=user_id)
    try:
        bot.edit_message_reply_markup(message.chat.id, message_id=message.message_id - 1, reply_markup=None)
    except:
        pass
    bot.send_message(message.chat.id, anek_text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'button1':
        markup = create_inline_keyboard()
        user_id = call.message.chat.id
        anek_text = db.get_unique_anek(user_id=user_id)
        bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        bot.send_message(call.message.chat.id, anek_text, reply_markup=markup)


bot.infinity_polling()

if __name__ == '__main__':
    bot.polling(none_stop=True)
