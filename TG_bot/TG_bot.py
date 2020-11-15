import telebot
from telebot import types
import config

bot = telebot.TeleBot(config.TOKEN)

keyboard=telebot.types.ReplyKeyboardMarkup()
keyboard.row('1','2','3','4','5','6')

@bot.message_handler(commands = ['start'])
def start(message):
    
    """
       Shows an welcome message and help info about the available commands.
    """
    me = bot.get_me()

    # Welcome message
    msg = ('''Hello!
I'm {0} and I came here to help you.
What would you like to do?''').format(me.first_name)
    bot.send_message(message.chat.id,msg,reply_markup=keyboard)
       




attemps=0
password=370920
@bot.message_handler(commands=['admin'])# блок для админа
def subscribe_chat(message):  
    bot.reply_to(message, "Enter team secret phrase:")
    global attemps
    attemps+=1

@bot.message_handler(func=lambda message: attemps==1)
def team_user_login(message):
    if message.text == password:
        bot.reply_to(message, "accepted")
    else:
        bot.reply_to(message, "Wrong secrete phrase, try again")
        global attemps
        attemps=0
        
        

bot.polling(none_stop = True)