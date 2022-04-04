# Импортируем необходимые классы.
import random

from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
from _datetime import datetime
from telegram import ReplyKeyboardMarkup


reply_keyboard = [['/dice', '/timer', '/rullete']]
general = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
Whatcubes = [['/roll_one_six_sided_die'], ['/roll_two_six_sided_die'],
             ['/roll_one_twenty_sided_die'], ['/back']]
cubes = ReplyKeyboardMarkup(Whatcubes, one_time_keyboard=False)
What_time = [['/set 30', '/set 60'], ['/set 300', '/back']]
set_time = ReplyKeyboardMarkup(What_time, one_time_keyboard=False)
close = ReplyKeyboardMarkup([['/unset']], one_time_keyboard=False)



# Напишем соответствующие функции.
# Их сигнатура и поведение аналогичны обработчикам текстовых сообщений.
def start(update, context):
    update.message.reply_text(
        "Я бот-справочник. Какая информация вам нужна?",
        reply_markup=general
    )


def help(update, context):
    update.message.reply_text(
        "Я пока не умею помогать... Я только ваше эхо.")


def nowDate(update, context):
    update.message.reply_text(f"{datetime.now().date()}")


def nowTime(update, context):
    update.message.reply_text(f"{datetime.now().time()}")


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


def dice(update, context):
    update.message.reply_text(
        "Выбирай кубик, ничтожество-_-",
        reply_markup=cubes
    )


def what_want_time(update, context):
    update.message.reply_text(
        "Выбирай время, ничтожество-_-",
        reply_markup=set_time
    )


def one_cube(update, context):
    update.message.reply_text(
        f"{random.randrange(0, 6)}")


def two_cube(update, context):
    update.message.reply_text(
        f"{random.randrange(0, 6)} и {random.randrange(0, 6)}")


def one_20_cube(update, context):
    update.message.reply_text(
        f"{random.randrange(0, 20)}")


def back(update, context):
    update.message.reply_text(
        "Ну и пока:(", reply_markup=general)


def echo(update, context):
    update.message.reply_text("Я получил сообщение: " + update.message.text)


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


def main():
    updater = Updater('5222085503:AAEOod2NrPTQv8NZG7BxD9977Kw-kL7ahLY', use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("date", nowDate))
    dp.add_handler(CommandHandler("time", nowTime))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(CommandHandler("dice", dice))
    dp.add_handler(CommandHandler("roll_one_six_sided_die", one_cube))
    dp.add_handler(CommandHandler("roll_two_six_sided_die", two_cube))
    dp.add_handler(CommandHandler("roll_one_twenty_sided_die", one_20_cube))
    dp.add_handler(CommandHandler("back", back))
    dp.add_handler(CommandHandler("timer", what_want_time))


    text_handler = MessageHandler(Filters.text, echo)

    dp.add_handler(CommandHandler("set", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("unset", unset_timer,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("rullete", rus_rullete,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))

    dp.add_handler(text_handler)

    updater.start_polling()

    updater.idle()



# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()