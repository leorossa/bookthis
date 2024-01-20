#!/usr/bin/env python

import sqlite3
import random
from telegram import Update
from telegram.ext import ContextTypes
from tmdbv3api import TMDb, Movie

from basekeyboard import text_help


tmdb = TMDb()
tmdb.api_key = "95982a3f170dcc7789a72455024860b2"
tmdb.language = 'ru'
movie = Movie()

#вынесение повторющегося текста в отдельную переменную


async def random_film(update: Update, context: ContextTypes.DEFAULT_TYPE):
        choice = update.message.text
        try:
            if choice == "Один случайный фильм":
                conn = sqlite3.connect('films.db')
                cursor = conn.cursor()
                cursor.execute('SELECT film FROM films WHERE user_id = ?', (update.effective_user.id,))
                films = cursor.fetchall()
                conn.close()
        
                if not films:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_help)
                else:
                    random_film = random.choice(films)
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Случайный фильм: {random_film[0]}")
    
            elif choice == "Последние 5 добавленных":
                conn = sqlite3.connect('films.db')
                cursor = conn.cursor()
                cursor.execute('SELECT film FROM films WHERE user_id = ? ORDER BY id DESC LIMIT 5', (update.effective_user.id,))
                films = cursor.fetchall()
                conn.close()
        
                if not films:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_help)
                else:
                    films_list = "\n".join([film[0] for film in films])
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Последние 5 добавленных фильмов:\n{films_list}")
        except Exception as e:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Неизвестная ошибка при рекомендации фильма\
                                           Посмотри в oneorfiverandom")