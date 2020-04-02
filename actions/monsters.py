import config
from database import db_agent
from utils import Mob, restricted

db = db_agent(config.db_name)


@restricted
def monsters_list(update, context):

    all_monsters = [el[0] for el in db.select_all_mobs()]

    update.message.reply_text('Доступные монстры:')
    update.message.reply_text('\n'.join(all_monsters).title())


@restricted
def monster_info(update, context):

    mobs = [el[0] for el in db.select_all_mobs()]
    mob = ' '.join(context.args).lower()
    if mob == '':
        update.message.reply_text('Напиши название монстра после команды!')
    elif mob in mobs:
        mobname = Mob(mob)
        update.message.reply_text('<b>{}</b>:\n{}'.format(mobname.rus_name.title(), mobname.mobinfo()), parse_mode='html')
    elif mob not in mobs:
        update.message.reply_text('Нет такого монстра!')
