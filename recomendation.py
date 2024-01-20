#!/usr/bin/env python

from telegram import Update
from telegram.ext import ContextTypes
from tmdbv3api import TMDb, Movie

from basekeyboard import reply_sim_rec_keyboard

tmdb = TMDb()
tmdb.api_key = "95982a3f170dcc7789a72455024860b2"
tmdb.language = 'ru'
movie = Movie()


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    movies = movie.search(query.message.caption)
    first_result = movies[0]
    s = movie.similar(first_result.id)
    for result in s:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=result.title)









"""
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    s = movie.search(query.message.caption)
    first_result = s[0]
    recommendations = movie.recommendations(first_result.id)
    for recommendation in recommendations:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=recommendation.title)

    for recommendation in recommendations:
        try:
            if query.data == "Похожие":
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=\
                                             'https://www.themoviedb.org/t/p/w600_and_h900_bestv2/'\
                                                    + recommendation.poster_path, caption=recommendation.title,\
                                                            reply_markup=reply_sim_rec_keyboard)
            elif query.data == "Подробнее":
                await context.bot.send_message(chat_id=update.effective_chat.id, text=recommendation.overview)
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Нет рекомендаций")
        except Exception as e:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Неизвестная ошибка при рекомендации фильма\
                                           Посмотри в recomendation")
"""