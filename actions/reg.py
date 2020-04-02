import config

from database import db_agent
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler

db = db_agent(config.db_name)

ANSWER = range(1)


def reg(update, context):

    user = update.message.from_user

    if str(user.id) in str(db.check_user_id()):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Прошу прощения, {}, но мы уже знакомы😎'.format(update.message.from_user.first_name))
    else:
        # Don't forget to create config.py and add admin id variable there.
        context.bot.send_message(chat_id=config.admin,
                                 text='Запрос на регистрацию от пользователя:\n '
                                      'Имя: {}\n'
                                      'ID: {}'.format(update.message.from_user.first_name, update.message.chat.id))
        keyboard = [
            [
                InlineKeyboardButton('Да', callback_data='ACCEPT_BUTTON;{0};{1};{2}'.format(
                    update.message.chat.id, update.message.from_user.first_name, update.message.from_user.last_name)),
                InlineKeyboardButton('Нет', callback_data='DECLINE_BUTTON;{0};{1};{2}'.format(
                    update.message.chat.id, update.message.from_user.first_name, update.message.from_user.last_name)),
            ]
        ]

        markup = InlineKeyboardMarkup(keyboard)

        context.bot.send_message(chat_id=config.admin, text='Подтвердить?', reply_markup=markup)


def keyboard_callback_handler(update, context):

    query = update.callback_query
    data = query.data
    button_type, chat_id, user_first_name, user_last_name = data.split(';')

    chat_id = int(chat_id)
    user_first_name = str(user_first_name)
    user_last_name = str(user_last_name)
    message_id = update.effective_message.message_id

    user_info = [(
        user_first_name,
        '5',
        '5',
        '1',
        user_first_name,
        user_last_name,
        chat_id,
        '1',
        '0',
        '100'
    ),]

    if button_type == "ACCEPT_BUTTON":
        db.update_user_data(user_info)
        context.bot.edit_message_reply_markup(chat_id=config.admin, message_id=message_id)
        context.bot.send_message(chat_id=chat_id, text='Спасибо за регистрацию!\n'
                                                       'Напиши /start и начнем!')
        context.bot.send_message(chat_id=config.admin, text='✅ Регистрация одобрена')

        return ConversationHandler.END

    elif button_type == "DECLINE_BUTTON":
        context.bot.edit_message_reply_markup(chat_id=config.admin, message_id=message_id)
        context.bot.send_message(chat_id=chat_id, text='Прошу прощения, регистрация не одобрена')
        context.bot.send_message(chat_id=config.admin, text='❌ Регистрация не одобрена')

        return ConversationHandler.END

    else:
        context.bot.send_message(chat_id=user_info[0][6], text='Что-то пошло не так')
