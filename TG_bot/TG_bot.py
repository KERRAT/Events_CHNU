import telebot
import util
from telebot import types
import config
from config import adminlst, password, admin_id, config_id
from DB_Events import DB_Events as db
import sqlite3
from datetime import datetime
import julian



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
    
    with open('id.txt') as f:
        global fd
        fd=f.readlines()
    with open('id.txt','a') as f:
        if str(message.chat.id)+'\n' not in fd:
            f.write(str(message.chat.id)+'\n' )        


    
    

    keyboard = util.generate_keyboard('Events')
    bot.send_message(message.chat.id,msg,reply_markup=keyboard)



@bot.message_handler(commands=['addevent'])
def AddEvent(message):
    if message.chat.id not in adminlst:
        bot.send_message(message.chat.id,'Ця функція доступна тільки для адмінів')
               
    else:
        inf.clear()
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
    sent=bot.send_message(message.chat.id,'Введіть дату івенту в форматі "місяць/день/рік часи:хвилини:секунди" наприклад 09/19/18 13:55:26 ')
    bot.register_next_step_handler(sent,reg_date)
def reg_date(message):
    date_events=str(message.text)
    try:
        datetime_object = datetime.strptime(date_events, '%m/%d/%y %H:%M:%S')#преварщаем строку которую ввел пользователь в формат datetime
        jd =julian.to_jd(  datetime_object,fmt='jd')#из даты в формате datetime конвертируем в григорианськую дату
        inf.append(jd)
        sen=bot.send_message(message.chat.id,'Зберегти івент. Напишіть так/ні') 
        bot.register_next_step_handler(sen,save_events)
    except:
        bot.send_message(message.chat.id,'Ви ввели некоректну дату , подивіться будь ласка приклад')
def save_events(message): # функция в которм админ выбирает добавить елемнт в базу данных 
    if message.text == 'так':
        DB.add_Event(inf)
        bot.send_message(message.chat.id,'Івент збережено')
        """dt = julian.from_jd(inf[2], fmt='jd')
        with open('id.txt') as f:
            fd=f.readlines()
        for i in fd:
            if int(i) in adminlst:
                continue 
            bot.send_message(int(i),'''Добавлено новий івент!!!
{}
Посилання на івент:{}
Дата проведення:{}
'''.format(inf[0],inf[1],str(dt)[:16]))"""
        inf.clear()#очищаем список для повторного использования в будущем 
    else:
        inf.clear()



        

@bot.message_handler(commands=['del_event'])
def addEvent(message):
    if message.chat.id in adminlst:

        DB.clear_data_inline(message)
        @bot.callback_query_handler(lambda query: query.data in util.get_names_arr("clear", 1, 20))
        def process_callback(query):
            DB.delete_some_event(query, message)
            names = DB.ev_names();
            bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=util.generate_inline_keyboard_2d_array(1, 'clear', names))
    else:
        bot.send_message(message.chat.id,'Ця функція доступна тільки для адмінів')

@bot.message_handler(commands=['old_ev'])
def addEvent(message):
    names = DB.old_ev_names()
    bot.send_message(chat_id=message.chat.id,text="Виберіть івент", reply_markup=util.generate_inline_keyboard_2d_array(1, 'oldEv', names)) #створення інлайн клавіатури
    @bot.callback_query_handler(lambda query: query.data in util.get_names_arr("oldEv", 0, 10)) #прийом колбеку при натисканні на клавіатуру
    def process_callback(query):
        names = DB.old_ev_names()
        DB.send_Ev(names[ord(query.data[6])-1][0], query.from_user.id) #перехід до функції відправки повідомленя



@bot.message_handler(content_types=["text"])
def event_button(message):
    if(message.text == 'Events'):
        names = DB.ev_names_sorted()
        print(message.chat.id)
        bot.send_message(chat_id=message.chat.id,text="Виберіть івент", reply_markup=util.generate_inline_keyboard_2d_array(1, 'event', names)) #створення інлайн клавіатури
        @bot.callback_query_handler(lambda query: query.data in util.get_names_arr("event", 0, 10)) #прийом колбеку при натисканні на клавіатуру
        def process_callback(query):
            names = DB.ev_names()
            DB.send_Ev(names[ord(query.data[6])-1][0], query.from_user.id) #перехід до функції відправки повідомленя
    if(message.text == 'Guides'):
        bot.send_message(message.chat.id, '4321')
       



bot.polling(none_stop = True)