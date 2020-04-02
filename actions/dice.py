import random

def roll(update, context):
    # если 1 - красный куб
    # если 2 - зеленый куб
    # если 3 - белый куб
    a = random.randint(1,3)

    if a == 1:
        update.message.reply_text('❤️')
    elif a == 2:
        update.message.reply_text('💛')
    elif a == 3:
        update.message.reply_text('💚')