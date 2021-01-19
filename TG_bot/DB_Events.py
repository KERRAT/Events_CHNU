import telebot
import util
from telebot import types
import config
from config import admin_id, config_id
import logging
import sqlite3
import json
import io
import pkgutil
import asyncio
import threading
import julian

conn = sqlite3.connect(":memory:", check_same_thread = False)  # настройки in memory бд

#создание класса базы данных
class DB_Events:
    def __init__(self):
        self.name = ""
        logging.basicConfig(level=logging.INFO)
        self.bot = telebot.TeleBot(config.TOKEN)
        self.cursor = conn.cursor()
        self.cursor.execute("CREATE TABLE Events (name TEXT, link TEXT, date INT)")
        self.data = self.get_data()
        for row in self.data:
            self.cursor.execute("INSERT INTO Events VALUES (?,?,?)", row)
    

#сохранение данных в файле базы данных
    def save_data(self):
        sql = "SELECT * FROM Events"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()  # or use fetchone()
        
        try:
            # Переводим словарь в строку
            str_data = json.dumps(data)
            print('{}'.format(str_data))
            # Обновляем  наш файл с данными
            self.bot.edit_message_media(media = types.InputMediaDocument(io.StringIO('{}'.format(str_data))), chat_id= admin_id, message_id= config_id)
        except Exception as ex:
            print(ex)

#получение данных с файла базы данных
    def get_data(self):
    # Пересылаем сообщение в данными от админа к админу
        forward_data = self.bot.forward_message(admin_id, admin_id, config_id)

    # Получаем путь к файлу, который переслали
        file_data = self.bot.get_file(forward_data.document.file_id)
        
    # Получаем файл по url
        file = self.bot.download_file(file_data.file_path)

    # Переводим данные из json в словарь и возвращаем
        return json.loads(file)


    """ Таймер
    def timer_start(self):
        threading.Timer(30.0, self.timer_start).start()
        try:
            asyncio.run_coroutine_threadsafe(self.save_data(),bot.loop)
        except Exception as exc:
            pass

"""


#получение списка ивентов
    def ev_names(self):
        self.cursor.execute("SELECT name FROM Events WHERE Events.date > julianday('now') ORDER BY date") 
        return self.cursor.fetchall()
    def add_name(self, name):
        print(name.text)

#введення данних в базу
    def add_Event(self, inf):
        self.cursor.execute("INSERT INTO Events VALUES (?,?,?)", inf)
        self.save_data()

# очищення данних з бази
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


#отправка сообщения с ивентом
    def send_Ev(self, name, message):
        self.cursor.execute("SELECT name, link, date FROM Events WHERE name = ?", [name]) #получение данных с базы данных
        data = self.cursor.fetchall()
        str = "{}".format(julian.from_jd(data[0][2]))
        msg = ('''{0}

Посилання на івент: {1}
Дата проведення: {2}''').format(data[0][0], data[0][1], str[:16])
        self.bot.send_message(message.chat.id,msg) #отправка сообщения с ивентом

        
#удаление ивентов
    def delete_some_event(self, q, mess):
        self.cursor.execute("DELETE FROM Events WHERE rowid = ?", "{}".format(ord(q.data[6])));
        self.save_data()
        self.bot.send_message(mess.chat.id,"Видалено!")