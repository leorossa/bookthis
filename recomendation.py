#!/usr/bin/env python
"""
from telegram import Update
from telegram.ext import ContextTypes
from tmdbv3api import TMDb, Movie

from basekeyboard import reply_rec_second_keyboard
from movie_saver import savefilm

#await context.bot.send_message(chat_id=update.effective_chat.id, text=)

tmdb = TMDb()
tmdb.api_key = "YOUR_API_KEY"
tmdb.language = 'ru'
movie = Movie()

#Берем название фильма из описания для постера фильма query.message.caption
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "Похожие":
        search = movie.search(query.message.caption)
        film = search[0]
        film_id = film.id
        similars = movie.similar(film_id)
        context.user_data['similars_list'] = list(similars)
        await send_similar_movie(update, context)  # Вызываем функцию для отправки первого фильма из similars_list
    elif query.data == "Далее":
        await send_next_similar_movie(update, context)
    elif query.data == "Сохранить":
        context.user_data["film"] = query.message.caption
        await savefilm(update, context)
    elif query.data == "Подробнее":
        film = query.message.caption
        search_film = movie.search(film)[0]
        await context.bot.send_message(chat_id=update.effective_chat.id, text=search_film.overview + "\n\n" +\
                                        "Средние оценки: " + str(search_film.vote_average))

async def send_similar_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    similars_list = context.user_data['similars_list']
    if similars_list:
        similar_movie = similars_list[0]  # Получаем первый фильм из similars_list
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=\
                                     'https://image.tmdb.org/t/p/w500/' +\
                                          similar_movie.poster_path, caption=similar_movie.title, \
                                            reply_markup=reply_rec_second_keyboard)
        if len(similars_list) > 1:
            context.user_data['similars_list'] = similars_list[1:]  # Обрезаем первый фильм из similars_list
        else:
            context.user_data.pop('similars_list', None)  # Удаляем similars_list из user_data, если список пустой

async def send_next_similar_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'similars_list' in context.user_data:
        await send_similar_movie(update, context)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Добавить логику рекомендаций из популярных кино")
"""
