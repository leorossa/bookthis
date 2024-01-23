#!/usr/bin/env python

from telegram import Update
from telegram.ext import ContextTypes
from tmdbv3api import TMDb, Movie

from movie_saver import savefilm
from found_movies import send_next_movie

tmdb = TMDb()
tmdb.api_key = "95982a3f170dcc7789a72455024860b2"
tmdb.language = 'ru'
movie = Movie()


async def button_inline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Сохраняет фильм"""
    query = update.callback_query
    await query.answer()
    if query.data == "Сохранить":
        context.user_data["film"] = query.message.caption
        await savefilm(update, context)

    elif query.data == "Подробнее":
        film = query.message.caption
        search_film = movie.search(film)[0]
        await context.bot.send_message(chat_id=update.effective_chat.id, text=search_film.overview + "\n\n" +\
                                        "Средние оценки: " + str(search_film.vote_average))

    elif query.data == "Далее":
        await send_next_movie(update, context)
    
    elif query.data == "Похожие":
        search = movie.search(query.message.caption)
        film = search[0]
        film_id = film.id
        similars = movie.similar(film_id)
        context.user_data['movies_list'] = list(similars)
        await send_next_movie(update, context)
    
    #elif query.data == "Развернуть":
    #    await 