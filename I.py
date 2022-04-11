import random

import requests
from General_Options import *
from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup


reply_keyboard = [['/dice', '/timer', '/rullete']]
general = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
Whatcubes = [['/roll_one_six_sided_die'], ['/roll_two_six_sided_die'],
             ['/roll_one_twenty_sided_die'], ['/back']]
cubes = ReplyKeyboardMarkup(Whatcubes, one_time_keyboard=False)
What_time = [['/set 30', '/set 60'], ['/set 300', '/back']]
set_time = ReplyKeyboardMarkup(What_time, one_time_keyboard=False)
close = ReplyKeyboardMarkup([['/unset']], one_time_keyboard=False)
comeback = ReplyKeyboardMarkup([['/back']], one_time_keyboard=False)


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
        f"How are you, {context.user_data['Name']}?")
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


def help(update, context):
    update.message.reply_text(
        "Я пока не умею помогать... Я только ваше эхо.")


def back(update, context):
    update.message.reply_text(
        "Ну и пока:(", reply_markup=general)


# Block for timer
def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


# Обычный обработчик, как и те, которыми мы пользовались раньше.
def set_timer(update, context):
    """Добавляем задачу в очередь"""
    chat_id = update.message.chat_id
    try:
        # args[0] должен содержать значение аргумента
        # (секунды таймера)
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text(
                'Извините, не умеем возвращаться в прошлое')
            return

        # Добавляем задачу в очередь
        # и останавливаем предыдущую (если она была)
        job_removed = remove_job_if_exists(
            str(chat_id),
            context
        )
        context.job_queue.run_once(
            task,
            due,
            context=chat_id,
            name=str(chat_id)
        )
        text = f'Вернусь через {due} секунд!'
        if job_removed:
            text += ' Старая задача удалена.'
        # Присылаем сообщение о том, что всё получилось.
        update.message.reply_text(text, reply_markup=close)

    except (IndexError, ValueError):
        update.message.reply_text('Использование: /set <секунд>')


def task(context):
    """Выводит сообщение"""
    job = context.job
    context.bot.send_message(job.context, text='Вернулся!')


def unset_timer(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Хорошо, вернулся сейчас!' if job_removed else 'Нет активного таймера.'
    update.message.reply_text(text, reply_markup=general)


def what_want_time(update, context):
    update.message.reply_text(
        "Выбирай время, ничтожество-_-",
        reply_markup=set_time
    )
# End block of timer


def dice(update, context):
    update.message.reply_text(
        "Выбирай кубик, ничтожество-_-",
        reply_markup=cubes
    )


def one_cube(update, context):
    update.message.reply_text(
        f"{random.randrange(1, 6)}")


def two_cube(update, context):
    update.message.reply_text(
        f"{random.randrange(1, 6)} и {random.randrange(0, 6)}")


def one_20_cube(update, context):
    update.message.reply_text(
        f"{random.randrange(1, 20)}")


def rus_rullete(update, context):
    try:
        pull = random.randrange(1, 6)
        die = int(context.args[0])
        if pull != die:
            update.message.reply_text("Тебе повезло, не сдох сегодня", reply_markup=general)
            print(pull)
        else:
            update.message.reply_text("Тебе не повезло, сдох сегодня", reply_markup=general)
            print(pull)
    except:
        update.message.reply_text("для использования введи: /rullete <число от 1 до 6>")


# Weather
def weather(update, context):
    try:
        geocoder_uri = geocoder_request_template = "http://geocode-maps.yandex.ru/1.x/"
        response = requests.get(geocoder_uri, params={
            "apikey": "8f291e24-fa66-4c82-81c9-cbf8e4a87a66",
            "format": "json",
            "geocode": update.message.text
        })

        toponym = response.json()["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        # print(((toponym['Point']['pos']).split(' '))[0])
        ll, spn = ((toponym['Point']['pos']).split(' '))[0], ((toponym['Point']['pos']).split(' '))[1]

        weather_api_reqest = \
            f'https://api.openweathermap.org/data/2.5/weather?lat={ll}&lon={spn}&appid=86269be3456b3b7a2752803a0eefcd22'
        weather_reqest = requests.get(weather_api_reqest)
        WeatherNow = weather_reqest.json()
        answer = (f'temperature in degrees Celsius: {int(WeatherNow["main"]["temp"]) - 273}' + '\n'
                  + f'wind speed: {WeatherNow["wind"]["speed"]} m/s' + '\n'
                  + f'main: {WeatherNow["weather"][0]["description"]}')
        update.message.reply_text(f'{answer}', reply_markup=general)
        return ConversationHandler.END
    except:
        update.message.reply_text('we could not find such a city, try again', reply_markup=general)
        return ConversationHandler.END


def WhatCity(update, context):
    update.message.reply_text('Name the city where you want to know the weather', reply_markup=comeback)
    return 1


def want_to_compare(update, context):
    update.message.reply_text('Name the city where you want to know the weather', reply_markup=comeback)


def main():
    updater = Updater('5222085503:AAEOod2NrPTQv8NZG7BxD9977Kw-kL7ahLY', use_context=True)

    dp = updater.dispatcher

    # dp.add_handler(CommandHandler("start", start))

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

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    weather_in_you_city = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('weather', WhatCity)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(Filters.text & ~Filters.command, weather)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(weather_in_you_city)
    dp.add_handler(conv_handler)

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

    text_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(text_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
