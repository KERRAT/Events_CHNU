import telebot
from telebot import types
import telegram
import config
from config import admin_id, config_id
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
        self.cursor.execute("CREATE TABLE users (chatid INTEGER , name TEXT, click INTEGER, state INTEGER)")
        self.get_data()
        self.cursor.execute("INSERT INTO users VALUES (1234, 'eee', 1,0)")
        self.save_data()
        self.conn.commit()
        sql = "SELECT * FROM users "
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        str_data = json.dumps(data)
        self.bot.send_document(message.chat.id, io.StringIO(str_data))
        self.bot.send_message(message.chat.id, 'admin_id = {}'.format(message.chat.id))
        self.bot.send_message(message.chat.id, 'config_id = {}'.format(message.message_id+2))
        
        
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
    def save_data(self):
        sql = "SELECT * FROM users "
        self.cursor.execute(sql)
        data = self.cursor.fetchall()  # or use fetchone()

        try:
            # Переводим словарь в строку
            str_data = json.dumps(data)
            # Обновляем  наш файл с данными
            self.bot.edit_message_media(media = types.InputMediaDocument(io.StringIO('{}'.format(str_data))), chat_id= admin_id, message_id= config_id)
        except Exception as ex:
            print(ex)
'''
    def get_data(self):
    # Пересылаем сообщение в данными от админа к админу
        forward_data = self.bot.forward_message(admin_id, admin_id, config_id)

    # Получаем путь к файлу, который переслали
        file_data = self.bot.get_file(forward_data.document.file_id)

    # Получаем файл по url
        file_url_data = self.bot.get_file_url(file_data.file_path)

    # Считываем данные с файла
        json_file= urlopen(file_url_data).read()

    # Переводим данные из json в словарь и возвращаем
        return json.loads(json_file)
    '''