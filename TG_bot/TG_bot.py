import telebot
import util
from telebot import types
import config
from config import adminlst, password, admin_id, config_id
from DB_Events import DB_Events as db
import sqlite3
import asyncio
import datetime




bot = telebot.TeleBot(config.TOKEN)


DB = db()

# DB.timer_start() Таймер вызов
inf=list()


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

@bot.message_handler(commands=['addevent'])
def AddEvent(message):
    if message.chat.id not in adminlst:
        bot.send_message(message.chat.id,'Ця функція доступна тільки для адмінів')
               
    else:
        sent=bot.send_message(message.chat.id,'Введіть назву івенту')
        bot.register_next_step_handler(sent,link)
        
def link (message):
    name_events=message.text
    inf.append(name_events)
    sent=bot.send_message(message.chat.id,'Введіть ссилку на статью')
    bot.register_next_step_handler(sent,date)
def date (message):
    link_events=message.text
    inf.append(link_events)
    sent=bot.send_message(message.chat.id,'Введіть дату івенту в форматі')
    bot.register_next_step_handler(sent,reg_date)
def reg_date(message):
    date_events=message.text
    inf.append(date_events)
    DB.add_Event(inf)
    inf.clear()










@bot.message_handler(commands=['clear_ALL_events'])
def addEvent(message):
    DB.clear_data_inline(message)
    @bot.callback_query_handler(lambda query: query.data in util.get_names_arr("clear", 0, 10))
    def process_callback(query):
        print(query.data)
        DB.delete_some_event(query)







@bot.message_handler(content_types=["text"])
def event_button(message):
    if(message.text == 'Events'):
        bot.send_message(chat_id=message.chat.id,text="Виберіть івент", reply_markup=util.generate_inline_keyboard_1d_array(1, 'ivent', (("Добрий день"), ("Зустріч"))))
    if(message.text == 'Guides'):
        bot.send_message(message.chat.id, '4321')
       



bot.polling(none_stop = True)