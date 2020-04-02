import config
import logging

from actions.start import start
from actions.heal import heal
from actions.player_info import player_info, change_player_name
from actions.unknown import unknown
from actions.fight import fight, turn, ask_answer, defense, done
from actions.monsters import monsters_list, monster_info
from actions.map import show_map
from actions.dice import roll
from actions.reg import reg, keyboard_callback_handler

from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler
from telegram.ext import CallbackQueryHandler
from database import db_agent

logging.basicConfig(level=logging.INFO)

db = db_agent(config.db_name)
FIGHT, TURN, ASK_ANSWER, DEFENSE = range(4)


def main():
    #Don't forget to insert YOUR TOKEN here)
    updater = Updater(token=config.token, use_context=True)
    dispatcher = updater.dispatcher

    # /start
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # /player_info
    player_info_handler = CommandHandler('player_info', player_info)
    dispatcher.add_handler(player_info_handler)

    # /monsters_list
    monsters_list_handler = CommandHandler('monster_list', monsters_list)
    dispatcher.add_handler(monsters_list_handler)

    # /monster_info
    monster_info_handler = CommandHandler('monster_info', monster_info)
    dispatcher.add_handler(monster_info_handler)

    # /change_player_name
    change_player_name_handler = CommandHandler('change_player_name', change_player_name)
    dispatcher.add_handler(change_player_name_handler)

    # /heal
    heal_handler = CommandHandler('heal', heal)
    dispatcher.add_handler(heal_handler)

    # /map
    map_handler = CommandHandler('map', show_map)
    dispatcher.add_handler(map_handler)

    # /roll
    dice_handler = CommandHandler('roll', roll)
    dispatcher.add_handler(dice_handler)

    # /fight
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('fight', fight)],
        states={

            TURN: [MessageHandler(Filters.text, turn)],
            ASK_ANSWER: [MessageHandler(Filters.text, ask_answer)],
            DEFENSE: [MessageHandler(Filters.text, defense)]
        },
        fallbacks=[CommandHandler('done', done)]
    )
    dispatcher.add_handler(conv_handler)

    # /reg
    reg_handler = CommandHandler('reg', reg)
    dispatcher.add_handler(reg_handler)

    # inline_keyboard_handler
    buttons_handler = CallbackQueryHandler(callback=keyboard_callback_handler, pass_chat_data=True)
    dispatcher.add_handler(buttons_handler)

    # /help
    help_handler = CommandHandler('help', start)
    dispatcher.add_handler(help_handler)

    # Unknown handlers
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

