from telegram import ReplyKeyboardMarkup

reply_keyboard = [['/dice', '/timer', '/rullete', '/weather', '/Iwiki', '/SeeSomeTerm']]
general = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
Whatcubes = [['/roll_one_six_sided_die'], ['/roll_two_six_sided_die'],
             ['/roll_one_twenty_sided_die'], ['/back']]
cubes = ReplyKeyboardMarkup(Whatcubes, one_time_keyboard=False)
What_time = [['/set 30', '/set 60'], ['/set 300', '/back']]
set_time = ReplyKeyboardMarkup(What_time, one_time_keyboard=False)
close = ReplyKeyboardMarkup([['/unset']], one_time_keyboard=False)
comeback = ReplyKeyboardMarkup([['/back']], one_time_keyboard=False)
yesornot = ReplyKeyboardMarkup([['yes'], ['nope']], one_time_keyboard=False)
Ok = ReplyKeyboardMarkup([['Ok']], one_time_keyboard=False)
Fine = ReplyKeyboardMarkup([['Fine']], one_time_keyboard=False)
ThatTerm = ReplyKeyboardMarkup([['Author', 'specific term']], one_time_keyboard=True)
