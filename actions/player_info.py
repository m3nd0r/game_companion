from utils import Player, restricted


@restricted
def player_info(update, context):
    player = Player(update.message.from_user.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text=player.player_info(), parse_mode='html')


@restricted
def change_player_name(update, context):
    player = Player(update.message.from_user.id)
    new_name = ' '.join(context.args)
    player.change_player_name(new_name, update.message.from_user.id)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Имя игрока изменено на: {}".format(new_name.title()))
