from utils import Player, restricted


@restricted
def heal(update, context):
    player = Player(update.message.from_user.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Исцеляю...".format(player.curr_hp))
    player.heal(update.message.from_user.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Готово!\n"
                                                                    "Текущие ХП: {}".format(player.curr_hp))