import telebot
import util
from telebot import types
import config
from config import adminlst, password, admin_id, config_id
from DB_Events import DB_Events as db
import sqlite3
import asyncio




bot = telebot.TeleBot(config.TOKEN)


DB = db()

# DB.timer_start() Таймер вызов


@bot.message_handler(commands = ['start'])
def start(message):
    
    """
       Shows an welcome message and help info about the available commands.
    """
        
    

    me = bot.get_me()
    msg = ('''Hello!
    I'm {0} and I came here to help you.
    What would you like to do?''').format(me.first_name)
    keyboard = util.generate_keyboard('Events', 'Guides')
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
    else:
        bot.reply_to(message, "Wrong secrete phrase, try again")
        global attemps
        attemps=0
   
@bot.message_handler(commands=['addevent'])
def AddEvent(message):
    sent = bot.send_message(message.chat.id, 'Please describe your problem.')
    bot.register_next_step_handler(sent, DB.add_name)

    sent = bot.send_message(message.chat.id, 'Please describe your')
    bot.register_next_step_handler(sent, DB.add_name)
    sent = bot.send_message(message.chat.id, 'Please describe')
    bot.register_next_step_handler(sent, DB.add_name)
    sent = bot.send_message(message.chat.id, 'Please')
    bot.register_next_step_handler(sent, DB.add_name)



@bot.message_handler(commands=['clear_ALL_events'])
def AddEvent(message):
    DB.clear_data_inline(message)
    @bot.callback_query_handler(lambda query: query.data in util.get_names_arr("clear", 0, 10))
    def process_callback(query):
        print(query.data)
        DB.delete_some_event(query)







@bot.message_handler(content_types=["text"])
def event_button(message):
    if(message.text == 'Events'):
        bot.send_message(chat_id=message.chat.id,text="Виберіть івент", reply_markup=util.generate_inline_keyboard_1d_array(1, 'ivent', ('123')))
    if(message.text == 'Guides'):
        bot.send_message(message.chat.id, '4321')
       



bot.polling(none_stop = True)