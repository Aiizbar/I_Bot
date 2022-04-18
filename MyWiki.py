import sqlite3

from flask import Flask
from telegram.ext import ConversationHandler

from option import *
from data import db_session
from data.Ipedia import Ipedia


def wikiGeneral(update, context):
    update.message.reply_text('We have created our own kind of wiki,\n'
                              ' you can add a term and describe it, since we do not have a moderator,\n'
                              ' we hope for your creativity', reply_markup=Ok)
    return 1


def WantToAddTerm(update, context):
    update.message.reply_text('want to add a new term?', reply_markup=yesornot)
    return 2


def OrNotWont(update, context):
    if update.message.text == 'yes':
        update.message.reply_text('enter term name', reply_markup=comeback)
        return 3
    if update.message.text == 'nope':
        update.message.reply_text('Ok', reply_markup=general)
        return ConversationHandler.END
    else:
        update.message.reply_text('You did not answer the question')
        return 1


def hendlerTerm(update, context):
    context.user_data['hendler'] = update.message.text
    update.message.reply_text('enter a description of the break')
    return 4


def generalInfo(update, context):
    context.user_data['generalInfo'] = update.message.text
    db_session.global_init("db/Iwiki.db")
    Mypedia = Ipedia()
    Mypedia.name = f"{context.user_data['Name']}"
    Mypedia.think = f"{context.user_data['hendler']}"
    Mypedia.about_think = f"{context.user_data['generalInfo']}"
    db_sess = db_session.create_session()
    db_sess.add(Mypedia)
    db_sess.commit()
    update.message.reply_text('Thanks for you job')
    return ConversationHandler.END


def WantToSeeTerm(update, context):
    update.message.reply_text('Do you want to see all the terms of one author or one particular term?', reply_markup=ThatTerm)
    return 1

def IwantToSeeTermOrAuthor(update, context):
    if update.message.text == 'specific term':
        update.message.reply_text('please enter the desired term')
        return 11
    elif update.message.text == 'Author':
        update.message.reply_text('please enter the desired Author')
        return 12
    else:
        update.message.reply_text("I don't have this function")
        return ConversationHandler.END


def VievAuthorTerm(update, context):
    con = sqlite3.connect('db/Iwiki.db')
    cur = con.cursor()
    try:
        result = cur.execute(f"""SELECT think, about_think FROM Iwiki where name = '{update.message.text}'""").fetchall()
        answer = ''
        for i, j in result:
            answer += str(i) + ' — ' + str(j) + '\n' + '\n'
        update.message.reply_text(f'{answer}\n'
                                  'thank you for using our Iwiki', reply_markup=general)
        return ConversationHandler.END
    except:
        update.message.reply_text('This term has not yet been added to our database.', reply_markup=comeback)
        return ConversationHandler.END


def VievSpecTerm(update, context):
    con = sqlite3.connect('db/Iwiki.db')
    cur = con.cursor()
    try:
        result = cur.execute(f"""SELECT think, about_think, name FROM Iwiki where think = '{update.message.text}'""").fetchall()
        update.message.reply_text(f'{result[0][0]} — {result[0][1]}, Author: {result[0][2]}', reply_markup=general)
        return ConversationHandler.END
    except:
        update.message.reply_text('This term has not yet been added to our database.', reply_markup=comeback)
        return ConversationHandler.END


def SeeName(update, context):
    update.message.reply_text(f'{context.user_data["Name"]}')