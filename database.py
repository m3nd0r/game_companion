import sqlite3
import random


class db_agent:

    def __init__(self, database):
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def select_all_mobs(self):
        """ Получаем всех мобов """
        with self.connection:
            return self.cursor.execute('SELECT name FROM mobs').fetchall()

    def select_mob(self, mobname):
        """ Получаем заданного монстра в виде tuple"""
        with self.connection:
            return self.cursor.execute('SELECT * FROM mobs WHERE name = ?', (mobname,)).fetchall()[0]

    def select_player(self, player_id):
        """Получаем параметры игрока в виде tuple"""
        with self.connection:
            return self.cursor.execute('SELECT * FROM player WHERE user_id = ?', (player_id, )).fetchone()

    def word_for_tr(self):
        """Получаем слово на английском для проверки"""
        with self.connection:
            return random.choice(self.cursor.execute('SELECT * FROM words').fetchall())

    def update_cur_hp(self, curr_hp, player_id):
        """Обновляем текущие ХП юзера"""
        with self.connection:
            return self.cursor.execute('UPDATE player SET curr_hp = ? WHERE user_id = ?', (int(curr_hp), (player_id),)).fetchall()

    def update_player_name(self, new_name, player_id):
        """Обновляем игровое имя текущего юзера"""
        with self.connection:
            return self.cursor.execute('UPDATE player SET name = ? WHERE user_id = ?', (str(new_name), (player_id),))

    def check_user_id(self):
        """Получаем список всех пользователей"""
        with self.connection:
            return self.cursor.execute('SELECT user_id FROM player').fetchall()

    def update_user_data(self, user_info):
        """Заносим данные пользователя из бота в БД"""
        with self.connection:
            return self.cursor.executemany('INSERT INTO player VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', user_info)

    def lvl_up(self, user_id):
        with self.connection:
            return self.cursor.execute("""UPDATE player SET lvl = lvl + 1 WHERE user_id = ?""", (user_id,))

    def set_exp_to_next_lvl(self):
        with self.connection:
            return self.cursor.execute("""UPDATE player
            SET exp_to_next_lvl = (SELECT leveling.exp FROM leveling WHERE leveling.lvl = player.lvl)""")

    def update_curr_exp(self, curr_exp, player_id):
        with self.connection:
            return self.cursor.execute('UPDATE player SET curr_exp = ? WHERE user_id = ?', (curr_exp, player_id,))

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()


"""    def get_player_lvl(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT lvl FROM player WHERE user_id = ?', (user_id,)).fetchone()

    def get_player_exp(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT curr_exp FROM player WHERE user_id = ?', (user_id,)).fetchone()"""

