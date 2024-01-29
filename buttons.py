#!/usr/bin/env python

from telegram import Update
from telegram.ext import ContextTypes
from tmdbv3api import TMDb, Movie

from movie_saver import savefilm
from found_movies import send_recomendation, send_overwiev, send_next_movie

tmdb = TMDb()
tmdb.api_key = "95982a3f170dcc7789a72455024860b2"
tmdb.language = 'ru'
movie = Movie()


async def button_inline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    query = update.callback_query
    await query.answer()
    """Сохраняет фильм"""
    if query.data == "Сохранить":
        context.user_data['title']
        await savefilm(update, context)

    elif query.data == "Далее":
        """Листаем список и удаляем прошлое сообщение"""
        await send_next_movie(update, context)
        await update.callback_query.message.delete()
    
    elif query.data == "Рекомендации":
        await send_recomendation(update, context)
        await update.callback_query.message.delete()

    elif query.data == "Понятно":
        await update.callback_query.message.delete()
    
    elif query.data == "Подробнее":
        await send_overwiev(update, context)
        await update.callback_query.message.delete()