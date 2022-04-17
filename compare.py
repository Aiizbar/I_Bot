from option import *


def want_to_compare(update, context):
    update.message.reply_text('Name the city where you want to know the weather', reply_markup=comeback)
    return 1


def first_word(update, context):
    context.user_data['FirstWord'] = update.message.text
    update.message.reply_text('this function allows you to compare texts by entering the first sentence')


def second_word(update, context):
    context.user_data['SekondWord'] = update.message.text