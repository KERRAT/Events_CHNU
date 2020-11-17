import telebot
from telebot import types
import config
from config import adminlst
from config import password
import DB_class
import logging
import pydispatch
from pydispatch import Dispatcher


bot = telebot.TeleBot(config.TOKEN)

keyboard=telebot.types.ReplyKeyboardMarkup()
keyboard.row('1','2','3','4','5','6')

DB = DB_class.DB()


@bot.message_handler(commands = ['start'])
def start(message):
    
    """
       Shows an welcome message and help info about the available commands.
    """
    DB.DB_connect(message)
    me = bot.get_me()

    # Welcome message
    msg = ('''Hello!
    I'm {0} and I came here to help you.
    What would you like to do?''').format(me.first_name)
    bot.send_message(message.chat.id,msg,reply_markup=keyboard)
       


attemps=0


@bot.message_handler(commands=['admin'])# блок для админа
def subscribe_chat(message):
    if message.chat.id in adminlst:
        bot.send_message(message.chat.id,'Привіт шановний адміне')  
    else:
        bot.reply_to(message, "Enter team secret phrase:")
        global attemps
        attemps+=1

@bot.message_handler(func=lambda message: attemps==1)
def team_user_login(message):
    global adminlst
    if message.text == password:
        adminlst.append(message.chat.id)
        bot.reply_to(message, "accepted")
        DB.DB_admin_connect(message)
    else:
        bot.reply_to(message, "Wrong secrete phrase, try again")
        global attemps
        attemps=0
        
        

bot.polling(none_stop = True)