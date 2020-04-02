from utils import restricted


@restricted
def show_map(update, context):
    update.message.reply_text('🗺Карта <b>Нового Мира:</b>', parse_mode='html')
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('images/map_1.jpg', 'rb'))
