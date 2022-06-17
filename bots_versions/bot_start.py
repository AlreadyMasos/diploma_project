from trackers import sq_track_class
from telegram.ext import *
import sqlite3 as sq
TOKEN = '5136769032:AAFkhfzSuJ7eKdnL2f46nWYqncyMk6hnK5I'

squats_counter = 0
pushups_counter = 0

def start(update, context):
    update.message.reply_text('''Отправьте этому боту видео,
на котором вы выполняете физическое упражнение.
Бот произведет анализ и назовет количество повторений
для тех упражнений, которые он умеет определять''')

def helper(update, context):
    update.message.reply_text('''
        /start - начать работу
        /help - помощь с командами
        ''')

def squats(update,context):
    
    global squats_counter
    squats_counter = sq_track_class.all_track(context.bot.get_file(
                                            update.message.video).download())
    update.message.reply_text('количество приседаний на видео: '+ str(
        squats_counter[1]) + '\n' + 'кол-во отжиманий: ' + str(
            squats_counter[0]
        ))
    
"""    
def pushups(update,context):
    global pushups_counter
    pushups_counter = sq_track_class.pushups_track(context.bot.get_file(
                                            update.message.video).download())
    update.message.reply_text('количество отжиманий на видео: ' +str(
        pushups_counter))"""

def show_users(update,context):
    with sq.connect('alldata.db') as con:
        cur = con.cursor()
        b = cur.execute('''SELECT user_name FROM USERS''').fetchall()
        update.message.reply_text(b, update.message.chat.id)

def add_user(update,context):
    with sq.connect('alldata.db') as con:
        cur = con.cursor()
        b = cur.execute('''INSERT INTO users VALUES (?,?)''')
        

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('help', helper))

dp.add_handler(MessageHandler(Filters.video, squats))
#dp.add_handler(MessageHandler(Filters.video, pushups))
dp.add_handler(CommandHandler('show_users',show_users))

updater.start_polling()
updater.idle()
