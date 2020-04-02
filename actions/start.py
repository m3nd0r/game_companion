import config
import time
from database import db_agent
from utils import restricted

db = db_agent(config.db_name)


@restricted
def start(update, context):
    user = update.message.from_user

    if str(user.id) in str(db.check_user_id()) and str(user.id) != str(config.admin) and str(user.id) != str(config.alice)\
            and str(user.id) != str(config.nata):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Снова привет! Вот основные команды:\n\n"
                                      "/monster_list - показывает, с какими противниками ты уже можешь сражаться\n"
                                      "/monster_info имяМонстра - показывает информацию о конкретном монстре\n"
                                      "/fight имяМонстраНаАнглийском - начать бой с выбранным монстром\n"
                                      "/player_info - узнать информацию о своем персонаже\n"
                                      "/change_player_name - изменить имя персонажа\n"
                                      "/heal - полностью вылечить своего персонажа\n"
                                      "/map - посмотреть на карту этого мира\n"
                                      "/roll - выбрать, насколько хорошее (или плохое) событие произойдёт"
                                 )

    elif user.id == config.admin:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Привет <b>Создатель</b>!✌🏻"
                                      "\nЕсли Алиска рядом, то можно начинать!",
                                 parse_mode='html')

    elif user.id == config.nata:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Натка?")
        time.sleep(1)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="😍")
        time.sleep(1)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Ты как всегда великолепна!")
        time.sleep(1)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Твой муж меня уже кое чему научил, поэтому запоминай основные команды:\n"
                                      "/monster_list - показывает, с какими противниками ты уже можешь сражаться\n"
                                      "/monster_info имяМонстра - показывает информацию о конкретном монстре\n"
                                      "/fight имяМонстраНаАнглийском - начать бой с выбранным монстром\n"
                                      "/player_info - узнать информацию о своем персонаже\n"
                                      "/change_player_name - изменить имя персонажа\n"
                                      "/heal - полностью вылечить своего персонажа\n"
                                      "/map - посмотреть на карту этого мира\n"
                                      "/roll - выбрать, насколько хорошее (или плохое) событие произойдёт")

    elif user.id == config.alice:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="🤨")
        time.sleep(1)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Алиска?")
        time.sleep(1)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="😧")
        time.sleep(1)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="🥳")
        time.sleep(1)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="😍")
        time.sleep(1)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Рад тебя видеть!!!")
        time.sleep(1)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Твой папа меня уже кое чему научил, поэтому запоминай основные команды:\n"
                                      "/monster_list - показывает, с какими противниками ты уже можешь сражаться\n"
                                      "/monster_info имяМонстра - показывает информацию о конкретном монстре\n"
                                      "/fight имяМонстраНаАнглийском - начать бой с выбранным монстром\n"
                                      "/player_info - узнать информацию о своем персонаже\n"
                                      "/change_player_name - изменить имя персонажа\n"
                                      "/heal - полностью вылечить своего персонажа\n"
                                      "/map - посмотреть на карту этого мира\n"
                                      "/roll - выбрать, насколько хорошее (или плохое) событие произойдёт")

    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Привет, {}!✌🏻".format(update.message.from_user.first_name))
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Я ещё молодой, но уже кое что могу, поэтому запоминай основные команды:\n"
                                      "/monster_list - показывает, с какими противниками ты уже можешь сражаться\n"
                                      "/monster_info имяМонстра - показывает информацию о конкретном монстре\n"
                                      "/fight имяМонстраНаАнглийском - начать бой с выбранным монстром\n"
                                      "/player_info - узнать информацию о своем персонаже\n"
                                      "/change_player_name - изменить имя персонажа\n"
                                      "/heal - полностью вылечить своего персонажа\n"
                                      "/map - посмотреть на карту этого мира\n"
                                      "/roll - выбрать, насколько хорошее (или плохое) событие произойдёт")


