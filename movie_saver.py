#!/usr/bin/env python

import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from tmdbv3api import TMDb, Movie

from basekeyboard import reply_sim_rec_keyboard

tmdb = TMDb()
tmdb.api_key = "95982a3f170dcc7789a72455024860b2"
tmdb.language = 'ru'
movie = Movie()


async def savefilm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    film = update.message.text
    search_film = movie.search(film)
    conn = sqlite3.connect('films.db')
    cursor = conn.cursor()

    try:
        if search_film:

            movies = search_film[0]
            cursor.execute('SELECT COUNT(*) FROM films WHERE user_id = ? AND film = ?',\
                           (update.effective_user.id, movies.title))
            count = cursor.fetchone()[0]

            if count == 0:
                cursor.execute('INSERT INTO films (user_id,film) VALUES (?, ?)',
                               (update.effective_user.id, movies.title))
                conn.commit()
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=\
                                             'https://www.themoviedb.org/t/p/w600_and_h900_bestv2/'\
                                                + movies.poster_path, caption=movies.title,\
                                                        reply_markup=reply_sim_rec_keyboard)
            else:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=\
                                             'https://www.themoviedb.org/t/p/w600_and_h900_bestv2/'\
                                                + movies.poster_path, caption=movies.title,\
                                                    reply_markup=reply_sim_rec_keyboard)
        
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Фильм не найден")
    except Exception as e:
        conn.rollback()
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Неизвестная ошибка при сохранении фильма\
                                       Посмотри в movie_saver")
    finally:
        conn.close()