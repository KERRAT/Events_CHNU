import telebot
import util
from telebot import types
import config
from config import admin_id, config_id, admin_ids, config_ids
import logging
#import pydispatch
#from pydispatch import Dispatcher
import sqlite3
import json
import io
import pkgutil
import asyncio
import threading

conn = sqlite3.connect(":memory:", check_same_thread = False)  # настройки in memory бд


class DB:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.bot = telebot.TeleBot(config.TOKEN)
        #self.dp = Dispatcher(self.bot)
        self.cursor = conn.cursor()
        self.cursor.execute("CREATE TABLE Events (name TEXT, pic TEXT, text TEXT)")
        self.data = self.get_data()
        for row in self.data:
            self.cursor.execute("INSERT INTO Events VALUES (?,?,?)", row)


        
    def DB_connect(self):
        print("1234")


    def save_data(self):
        sql = "SELECT * FROM Events"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()  # or use fetchone()

        try:
            # Переводим словарь в строку
            str_data = json.dumps(data)
            # Обновляем  наш файл с данными
            self.bot.edit_message_media(media = types.InputMediaDocument(io.StringIO('{}'.format(str_data))), chat_id= admin_id, message_id= config_id)
        except Exception as ex:
            print(ex)

    def get_data(self):
    # Пересылаем сообщение в данными от админа к админу
        forward_datas = self.bot.forward_message(admin_ids, admin_ids, config_ids)
        forward_data= self.bot.forward_message(admin_id, admin_id, config_id)
    # Получаем путь к файлу, который переслали
        file_data = self.bot.get_file(forward_data.document.file_id)
        file_datas=self.bot.get_file(forward_datas.document.file_id)
    # Получаем файл по url
        file = self.bot.download_file(file_data.file_path)
        files = self.bot.download_file(file_datas.file_path)
    # Переводим данные из json в словарь и возвращаем
        return json.loads(file) and json.loads(files)
        




    def timer_start(self):
        threading.Timer(30.0, self.timer_start).start()
        try:
            asyncio.run_coroutine_threadsafe(self.save_data(),bot.loop)
        except Exception as exc:
            pass


    def add_TEXT(self, message):
        self.cursor = conn.cursor()
        self.cursor.execute("INSERT INTO Events VALUES ('{}', 'fwef', 'fwedg')".format(message.text))
        self.save_data()

    def clear_data_inline(self, message):
        sql = "SELECT name FROM Events"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()  # or use fetchone()
        listOfNames = list()
        for row in data:
            for name in row:
                listOfNames.append(name)
        keyboard = util.generate_inline_keyboard_1d_array(2, 'clear', listOfNames)
        self.bot.send_message(message.chat.id,'Виберіть що удалити:',reply_markup=keyboard)

    def delete_some_event(self, q):
        self.bot.send_message(q.message.chat.id, "123")
        self.cursor.execute("DELETE FROM Events WHERE rowid = {}".format( q.data[6]))
        self.save_data()


