import telebot
import util
from telebot import types
import config
from config import admin_id, config_id
import logging
import pydispatch
import sqlite3
import json
import io
import pkgutil
import asyncio
import threading

conn = sqlite3.connect(":memory:", check_same_thread = False)  # настройки in memory бд


class DB_Guides:
    def __init__(self):
        self.name = ""
        logging.basicConfig(level=logging.INFO)
        self.bot = telebot.TeleBot(config.TOKEN)
        self.cursor = conn.cursor()
        self.cursor.execute("CREATE TABLE Events (name TEXT, pic TEXT, text TEXT)")
        self.data = self.get_data()
        for row in self.data:
            self.cursor.execute("INSERT INTO Events VALUES (?,?,?)", row)
