from telegram.ext import ConversationHandler

from option import *


def start(update, context):
    update.message.reply_text(
        "Ohae oni chan(((0)))(((0))). First, tell us a little about yourself\n"
        "You can abort the poll by sending the command /stop.\n"
        "How can I call you?")

    # Число-ключ в словаре states —
    # втором параметре ConversationHandler'а.
    return 1
    # Оно указывает, что дальше на сообщения от этого пользователя
    # должен отвечать обработчик states[1].
    # До этого момента обработчиков текстовых сообщений
    # для этого пользователя не существовало,
    # поэтому текстовые сообщения игнорировались.


def echo(update, context):
    update.message.reply_text("what are you carrying?")


def first_response(update, context):
    # Это ответ на первый вопрос.
    # Мы можем использовать его во втором вопросе.
    context.user_data['Name'] = update.message.text
    update.message.reply_text(
        f"How are you, {context.user_data['Name']}?", reply_markup=Fine)
    # Следующее текстовое сообщение будет обработано
    # обработчиком states[2]
    return 2


def second_response(update, context):
    # Ответ на второй вопрос.
    # Мы можем его сохранить в базе данных или переслать куда-либо.
    weather = update.message.text
    # logger.info(weather)
    update.message.reply_text("Well, lest you tell me anyway, hold the main menu:", reply_markup=general)
    return ConversationHandler.END  # Константа, означающая конец диалога.
    # Все обработчики из states и fallbacks становятся неактивными.


def stop(update, context):
    update.message.reply_text("Ok, gooddie", reply_markup=general)
    return ConversationHandler.END
# End of starting qwestion


def what_want_time(update, context):
    update.message.reply_text(
        "Выбирай время, ничтожество-_-",
        reply_markup=set_time
    )


def help(update, context):
    update.message.reply_text(
        f"How I can help, {context.user_data['Name']}?")


def back(update, context):
    update.message.reply_text(
        "Gooddie:(", reply_markup=general)
    return ConversationHandler.END