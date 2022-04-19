from option import *


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
                "Sorry, we can't go back in time")
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
        text = f"I'll be back in {due} seconds!"
        if job_removed:
            text += 'The old task has been removed.'
        # Присылаем сообщение о том, что всё получилось.
        update.message.reply_text(text, reply_markup=close)

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')


def task(context):
    """Выводит сообщение"""
    job = context.job
    context.bot.send_message(job.context, text='returned!')


def unset_timer(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Okay, back now!' if job_removed else 'There is no active timer.'
    update.message.reply_text(text, reply_markup=general)