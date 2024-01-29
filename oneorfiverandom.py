#!/usr/bin/env python

import sqlite3
import random
from telegram import Update
from telegram.ext import ContextTypes

from basekeyboard import text_help, reply_pon_keyboard, reply_details_keyboard


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
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_help,\
                                                    reply_markup=reply_pon_keyboard)
                else:
                    random_movie = random.choice(films)
                    context.user_data['overview_movies'] = random_movie[0]
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Случайный фильм: {random_movie[0]}",\
                                                    reply_markup=reply_details_keyboard)
    
            elif choice == "Последние 5 добавленных":
                conn = sqlite3.connect('films.db')
                cursor = conn.cursor()
                cursor.execute('SELECT film FROM films WHERE user_id = ? ORDER BY id DESC LIMIT 5', (update.effective_user.id,))
                films = cursor.fetchall()
                conn.close()
        
                if not films:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_help,\
                                                    reply_markup=reply_pon_keyboard)
                else:
                    films_list = "\n".join([film[0] for film in films])
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Последние 5 добавленных фильмов:\n{films_list}",\
                                                    reply_markup=reply_pon_keyboard)
        except Exception as e:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Неизвестная ошибка при рекомендации фильма\
                                           Посмотри в oneorfiverandom", reply_markup=reply_pon_keyboard)