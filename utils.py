from database import db_agent
from functools import wraps

import config
import operator
import random

db = db_agent(config.db_name)


def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):

        user_id = update.effective_user.id
        if str(user_id) not in str(db.check_user_id()):
            update.message.reply_text('Прошу прощения, но я Вас не знаю...\n'
                                      'Напишите /reg для запроса регистрации')
            print(user_id)
            return
        return func(update, context, *args, **kwargs)
    return wrapped


class CalcGenerator:

    def __init__(self):
        self.ops = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
    }

    def rand_calc(self, difficulty):
        a = random.randint(2, 10)
        b = random.randint(2, 10)
        c = random.randint(2, 10)
        op = random.choice(list(self.ops.keys()))
        if difficulty == 1:
            if a > b:
                answer = self.ops['*'](a, b)
                operation = {'{} {} {} ='.format(a, '*', b): answer}
            else:
                answer = self.ops['*'](b, a)
                operation = {'{} {} {} ='.format(b, '*', a): answer}

            return operation

        elif difficulty == 2:
            if a > b:
                answer_1 = self.ops['*'](a, b)
                if answer_1 < c:
                    answer_2 = self.ops.get(op)(c, answer_1)
                else:
                    answer_2 = self.ops.get(op)(answer_1, c)

                operation = {'{} {} {} {} {} ='.format(a, '*', b, op, c): answer_2}
            else:
                answer_1 = self.ops['*'](b, a)
                if answer_1 < c:
                    answer_2 = self.ops.get(op)(c, answer_1)
                else:
                    answer_2 = self.ops.get(op)(answer_1, c)

                operation = {'{} {} {} {} {} ='.format(b, '*', a, op, c): answer_2}

            return operation


class Mob:

    def __init__(self, name):
        mob_info = db.select_mob(name)
        self.name = mob_info[1]
        self.hp = mob_info[2]
        self.dmg = mob_info[3]
        self.difficulty = mob_info[4]
        self.rus_name = mob_info[5]
        self.exp = mob_info[6]

    def mobinfo(self):
        return "🔸Количество ХП: {}\n🔸Урон: {}".format(self.hp, self.dmg)


class Player:

    def __init__(self, player_id):
        player_stats = db.select_player(player_id)

        self.name = player_stats[1]
        self.max_hp = player_stats[2]
        self.curr_hp = player_stats[3]
        self.dmg = player_stats[4]
        self.first_name = player_stats[5]
        self.last_name = player_stats[6]
        self.user_id = player_stats[7]
        self.lvl = player_stats[8]
        self.curr_exp = player_stats[9]
        self.next_lvl_exp = player_stats[10]

    def player_info(self):
        info = "⚜️ <b>{}</b> ⚜️\n\n🔰 Уровень: {}\nСейчас опыта: {}\nОпыта до след. уровня: {}\n\n💚 Макс ХП: {}\n💛 Текущие ХП: {}\n⚔ Урон: {}\n".format(
            self.name, self.lvl, self.curr_exp, self.next_lvl_exp - self.curr_exp, self.max_hp, self.curr_hp, self.dmg
        )
        return info

    def update_hp(self, curr_hp, player_id):
        self.curr_hp = db.update_cur_hp(curr_hp, player_id)
        return self.curr_hp

    def heal(self, player_id):
        self.curr_hp = db.update_cur_hp(self.max_hp, player_id)
        self.curr_hp = self.max_hp

    def change_player_name(self, new_name, player_id):
        self.name = db.update_player_name(new_name, player_id)
        self.name = new_name

    def update_curr_exp(self, curr_exp, player_id):
        self.curr_exp = curr_exp
        db.update_curr_exp(curr_exp, player_id)
