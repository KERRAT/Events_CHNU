import telebot
from telebot import types
import DB_Events
from DB_Events import DB_Events as db
import config
from config import admin_id, config_id
import logging
import sqlite3
import json
import io
import pkgutil
import threading

bot = telebot.TeleBot(config.TOKEN)

def generate_keyboard (*answer):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for item in answer:
        button = types.KeyboardButton(item)
        keyboard.add(button)
    return keyboard

def generate_inline_keyboard (width, name, *answer):
    inline_keyboard = types.InlineKeyboardMarkup(row_width= width)
    i=1
    for text in answer:
         InlineButtonMainMenu = types.InlineKeyboardButton(text = text, callback_data = "{}_{}".format(name, chr(i)))
         inline_keyboard.add(InlineButtonMainMenu)
         i = i + 1
    return inline_keyboard

def generate_inline_keyboard_1d_array (width, name, *answer):
    inline_keyboard = types.InlineKeyboardMarkup(row_width= width)
    i=1
    for arr_1d in answer:
        for text in arr_1d:
            InlineButtonMainMenu = types.InlineKeyboardButton(text = text, callback_data = "{}_{}".format(name, chr(i)))
            inline_keyboard.add(InlineButtonMainMenu)
            i = i + 1
    return inline_keyboard

def generate_inline_keyboard_2d_array (width, name, *answer):
    inline_keyboard = types.InlineKeyboardMarkup(row_width= width)
    i=1
    for arr_2d in answer:
        for arr_1d in arr_2d:
            for text in arr_1d:
                InlineButtonMainMenu = types.InlineKeyboardButton(text = text, callback_data = "{}_{}".format(name, chr(i)))
                inline_keyboard.add(InlineButtonMainMenu)
                i = i + 1
    return inline_keyboard


def get_names_arr(name, beg, end):
    l = list()
    for x in range(beg,end):
        l.append("{}_{}".format(name, chr(x)))
    return l