from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram.ext import CallbackContext, CommandHandler

from Weather import *
from general import *
from time_in_bot import *
from Dice import *
from MyWiki import *


def main():
    updater = Updater('5222085503:AAEOod2NrPTQv8NZG7BxD9977Kw-kL7ahLY', use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('start', start)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(Filters.text & ~Filters.command, first_response)],
            # Функция читает ответ на второй вопрос и завершает диалог.
            2: [MessageHandler(Filters.text & ~Filters.command, second_response)]
        },

        # Точка прерывания диалога. В данном случае — команда /back.
        fallbacks=[CommandHandler('back', back)]
    )

    weather_in_you_city = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /weather. Она задаёт первый вопрос.
        entry_points=[CommandHandler('weather', WhatCity)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(Filters.text & ~Filters.command, weather)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('back', back)]
    )

    Wiki = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('Iwiki', wikiGeneral)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(Filters.text & ~Filters.command, WantToAddTerm)],
            2: [MessageHandler(Filters.text & ~Filters.command, OrNotWont)],
            3: [MessageHandler(Filters.text & ~Filters.command, hendlerTerm)],
            4: [MessageHandler(Filters.text & ~Filters.command, generalInfo)]
        },

        # Точка прерывания диалога. В данном случае — команда /back.
        fallbacks=[CommandHandler('back', back)]
    )

    SeeWikiTerm = ConversationHandler(
        entry_points=[CommandHandler('SeeSomeTerm', WantToSeeTerm)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(Filters.text & ~Filters.command, IwantToSeeTermOrAuthor)],
            11: [MessageHandler(Filters.text & ~Filters.command, VievSpecTerm)],
            12: [MessageHandler(Filters.text & ~Filters.command, VievAuthorTerm)]
        },

        # Точка прерывания диалога. В данном случае — команда /back.
        fallbacks=[CommandHandler('back', back)]
    )

    dp.add_handler(weather_in_you_city)
    dp.add_handler(conv_handler)
    dp.add_handler(Wiki)
    dp.add_handler(SeeWikiTerm)

    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("back", back))
    # Timer
    dp.add_handler(CommandHandler("set", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("unset", unset_timer,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("timer", what_want_time))
    # Dice
    dp.add_handler(CommandHandler("dice", dice))
    dp.add_handler(CommandHandler("roll_one_six_sided_die", one_cube))
    dp.add_handler(CommandHandler("roll_two_six_sided_die", two_cube))
    dp.add_handler(CommandHandler("roll_one_twenty_sided_die", one_20_cube))
    # Russian roulette
    dp.add_handler(CommandHandler("rullete", rus_rullete,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))

    dp.add_handler(CommandHandler("weather", WhatCity))

    dp.add_handler(CommandHandler("name", SeeName))

    text_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(text_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
