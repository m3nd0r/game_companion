import random
import config

from utils import Mob, Player, restricted
from utils import CalcGenerator
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from database import db_agent
from translation import translation

FIGHT, TURN, ASK_ANSWER, DEFENSE = range(4)

db = db_agent(config.db_name)

end_turn = ReplyKeyboardMarkup([['Завершить ход']], one_time_keyboard=True)
calc = CalcGenerator()


@restricted
def fight(update, context):

    mobs = [el[0] for el in db.select_all_mobs()]
    mob = ' '.join(context.args).lower()

    if mob in mobs:
        context.user_data['mobname'] = Mob(mob)
        mobname = context.user_data['mobname']
        update.message.reply_text('Твой противник: <b>{}</b>\n{}'.format(mobname.rus_name.title(), mobname.mobinfo()),
                                  reply_markup=ReplyKeyboardMarkup([['Вперёд⚔️']], one_time_keyboard=True),
                                  parse_mode='html')
        return TURN
    else:
        update.message.reply_text('Нет такого монстра!')


def turn(update, context):
    player = Player(update.message.from_user.id)
    mobname = context.user_data['mobname']
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='🔸ХП Игрока: {}\n🔸ХП Монстра: {}'.format(player.curr_hp, mobname.hp))
    # Определеяется сложность моба:
    difficulty = mobname.difficulty
    ops = calc.rand_calc(difficulty)
    for k, v in ops.items():
        operation = k
        answer = v
        context.user_data['answer'] = answer
        context.user_data['wrong_answers'] =[random.randint(int(answer), int(answer)+15) for i in range(3)]

        update.message.reply_text('<b>{}</b>'.format(operation), reply_markup=keyboard_generator(context),
                                  parse_mode='html')
        context.user_data['translation'] = db.word_for_tr()

    return ASK_ANSWER


def keyboard_generator(context):
    correct_answer = context.user_data['answer']
    wrong_answers = context.user_data['wrong_answers']

    all_answers = []
    for i in wrong_answers:
        all_answers.append(str(i))
    all_answers.append(str(correct_answer))
    random.shuffle(all_answers)

    all_answers_markup = ReplyKeyboardMarkup([all_answers], one_time_keyboard=True)

    return all_answers_markup


def ask_answer(update, context):
    player = Player(update.message.from_user.id)
    mobname = context.user_data['mobname']
    text = update.message.text

    if text == str(context.user_data['answer']):
        update.message.reply_text('<b>{}</b> получает <b>{}</b> урона'.format(mobname.rus_name.title(), player.dmg),
                                  parse_mode='html')
        mobname.hp -= player.dmg
        if mobname.hp <= 0:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='Противник повержен!\nОтличная битва!\n'
                                          '<b>Получено {} опыта.</b>'.format(mobname.exp), parse_mode='html',
                                     reply_markup=ReplyKeyboardRemove())
            new_exp = player.curr_exp + mobname.exp
            player.update_curr_exp(new_exp, update.message.from_user.id)

            if player.curr_exp > player.next_lvl_exp:
                db.lvl_up(update.message.from_user.id)
                db.set_exp_to_next_lvl()
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text='Поздравляем, вы получили уровень!', reply_markup=ReplyKeyboardRemove())
                return ConversationHandler.END
            else:
                return ConversationHandler.END
    else:
        update.message.reply_text('<b>Промах!</b>', parse_mode='html')

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Защищайся!')
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Переверди на русский: <b>{}</b>'.format(context.user_data['translation'][0]),
                             parse_mode="html")
    word = context.user_data['translation'][0]
    translations_list = translation(word)
    context.user_data['translations_list'] = translations_list

    return DEFENSE


def defense(update, context):
    player = Player(update.message.from_user.id)
    mobname = context.user_data['mobname']
    text = update.message.text
    context.user_data['player_translate'] = text
    player_translate = context.user_data['player_translate']

    if str(player_translate).lower() in context.user_data['translations_list']:
        update.message.reply_text('Защита успешна🛡',
                                  reply_markup=end_turn)
    else:
        update.message.reply_text('Неверно!\n'
                                  'Монстр наносит вам {} урона!'.format(mobname.dmg),
                                  reply_markup=end_turn)
        player.curr_hp -= mobname.dmg
        db.update_cur_hp(player.curr_hp, update.message.from_user.id)
        if player.curr_hp <= 0:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Битва проиграна😔\n'
                                                                            'Нужно лечение!', reply_markup=ReplyKeyboardRemove())

            return ConversationHandler.END

    return TURN


def done(update, context):
    update.message.reply_text('Завершение процесса...')
    return ConversationHandler.END
