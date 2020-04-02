from utils import restricted


@restricted
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Прости, не знаю такой команды 😔")
