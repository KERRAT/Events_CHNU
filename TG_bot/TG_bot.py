import telebot
from telebot import types
import config

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(content_types = ['text'])
def start(message):
    if(message.text == '/start'):
        """
           Shows an welcome message and help info about the available commands.
        """
        me = bot.get_me()

        # Welcome message
        msg = ("Hello!\n")
        msg += ("I'm {0} and I came here to help you.\n").format(me.first_name)
        msg += ("What would you like to do?\n\n")
        InlineKeyboardMainMenu = types.InlineKeyboardMarkup(row_width= 3)
        Inline1ButtonMainMenu = types.InlineKeyboardButton(text = "1", callback_data = "first")
        Inline2ButtonMainMenu = types.InlineKeyboardButton(text = "2", callback_data = "second")
        Inline3ButtonMainMenu = types.InlineKeyboardButton(text = "3", callback_data = "third")
        Inline4ButtonMainMenu = types.InlineKeyboardButton(text = "4", callback_data = "forse")
        Inline5ButtonMainMenu = types.InlineKeyboardButton(text = "5", callback_data = "fifth")
        Inline6ButtonMainMenu = types.InlineKeyboardButton(text = "6", callback_data = "sixth")
        InlineKeyboardMainMenu.add(Inline1ButtonMainMenu,
                                  Inline2ButtonMainMenu,
                                 Inline3ButtonMainMenu,
                                Inline4ButtonMainMenu,
                               Inline5ButtonMainMenu,
                              Inline6ButtonMainMenu)

        bot.send_message(chat_id=message.chat.id,
                        text=msg,
                        reply_markup=InlineKeyboardMainMenu) 
    else:
        lineKeyboardMainMenu = types.ReplyKeyboardMarkup(row_width= 3)
        line1ButtonMainMenu = types.KeyboardButton(text = "1")
        line2ButtonMainMenu = types.KeyboardButton(text = "2")
        line3ButtonMainMenu = types.KeyboardButton(text = "3")
        line4ButtonMainMenu = types.KeyboardButton(text = "4")
        line5ButtonMainMenu = types.KeyboardButton(text = "5")
        line6ButtonMainMenu = types.KeyboardButton(text = "6")
        lineKeyboardMainMenu.add(Inline1ButtonMainMenu,
                               Inline2ButtonMainMenu,
                              Inline3ButtonMainMenu,
                             Inline4ButtonMainMenu,
                            Inline5ButtonMainMenu,
                           Inline6ButtonMainMenu)
        bot.send_message(message.chat.id,
                        reply_markup=lineKeyboardMainMenu) 

bot.polling(none_stop = True)