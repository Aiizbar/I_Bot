import random
from option import *


def dice(update, context):
    update.message.reply_text(
        "Pick a dice, you jerk -_-",
        reply_markup=cubes
    )


def one_cube(update, context):
    update.message.reply_text(
        f"{random.randrange(1, 6)}")


def two_cube(update, context):
    update.message.reply_text(
        f"{random.randrange(1, 6)} и {random.randrange(1, 6)}")


def one_20_cube(update, context):
    update.message.reply_text(
        f"{random.randrange(1, 20)}")


def rus_rullete(update, context):
    try:
        pull = random.randrange(1, 6)
        die = int(context.args[0])
        if pull != die:
            update.message.reply_text("You're lucky you didn't die today", reply_markup=general)
            print(pull)
        else:
            update.message.reply_text("You're out of luck, died today", reply_markup=general)
            print(pull)
    except:
        update.message.reply_text("to use type: /rullete <number from 1 to 6>")