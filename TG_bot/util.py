import telebot
from telebot import types
import DB_class
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Bot

def generate_keyboard (*answer):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for item in answer:
        button = types.KeyboardButton(item)
        keyboard.add(button)
    return keyboard

def generate_inline_keyboard (width, name, *answer):
    inline_keyboard = types.InlineKeyboardMarkup(row_width= width)
    i=0
    for item in answer:
        InlineButtonMainMenu = types.InlineKeyboardButton(text = item, callback_data = "{}_{}".format(name, i))
        inline_keyboard.add(InlineButtonMainMenu)
    return inline_keyboard