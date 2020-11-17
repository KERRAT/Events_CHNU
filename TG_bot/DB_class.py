import telebot
from telebot import types
import config
import logging
import pydispatch
from pydispatch import Dispatcher
import sqlite3
import json
import io
import pkgutil

class DB:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.bot = telebot.TeleBot(config.TOKEN)
        self.dp = Dispatcher(self.bot)

    def DB_admin_connect(self,message):
        self.conn = sqlite3.connect(":memory:")  # настройки in memory бд
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE users (chatid INTEGER , name TEXT)")
        self.conn.commit()
        sql = "SELECT * FROM users "
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        str_data = json.dumps(data)
        self.bot.send_document(message.chat.id, io.StringIO(str_data))
        self.bot.send_message(message.chat.id, 'admin_id = {}'.format(message.chat.id))
        self.bot.send_message(message.chat.id, 'config_id = {}'.format(message.message_id+1))
        
        
    def DB_connect(self, message):
        self.conn = sqlite3.connect(":memory:")  # настройки in memory бд
        self.cursor = self.conn.cursor()
        try:
            sql = "SELECT * FROM users where chatid={}".format(message.chat.id)
            cursor.execute(sql)
            data = cursor.fetchone()  # or use fetchone()
        except Exception:
            data = self.cursor.fetchall()
            self.cursor.execute("CREATE TABLE users (chatid INTEGER , name TEXT, click INTEGER, state INTEGER)")
            self.cursor.executemany("INSERT INTO users VALUES (?,?,?,?)", data)
            self.conn.commit()
            sql = "SELECT * FROM users where chatid={}".format(message.chat.id)
            self.cursor.execute(sql)
            data = self.cursor.fetchone()  # or use fetchone()
