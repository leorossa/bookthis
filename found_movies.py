from telegram import Update
from telegram.ext import ContextTypes
from tmdbv3api import TMDb, Movie

from basekeyboard import reply_rec_second_keyboard, reply_sim_rec_keyboard

#Подключаемся к базе imdb
tmdb = TMDb()
tmdb.api_key = "95982a3f170dcc7789a72455024860b2"
tmdb.language = 'ru'
movie = Movie()

#Берем название фильма из описания для постера фильма query.message.caption
async def found_films(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    film = update.message.text #Ищем фильм в любом сообщении из чата пользователя кроме списка filter
    films = movie.search(film) #Ищем фильм в базе imdb по названию фильма films и возвращаем список с названиями
    context.user_data['movies_list'] = list(films) #Сохраняем список фильмов в user_data пользователя по ключу 'movies_list'
    await send_movie(update, context)

#отправка фильма пользователю
async def send_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movies_list = context.user_data['movies_list'] #Получаем список фильмов из user_data
    if len(movies_list) == 1: #Если список состоит из одного фильма
        movies = movies_list[0]
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=\
                                     'https://image.tmdb.org/t/p/w500/' +\
                                          movies.poster_path, caption=movies.title, \
                                            reply_markup=reply_sim_rec_keyboard)
    elif len(movies_list) > 0: #Если список не пустой
        movies = movies_list[0]  # Получаем первый фильм из movies_list
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=\
                                     'https://image.tmdb.org/t/p/w500/' +\
                                          str(movies.poster_path), caption=movies.title, \
                                            reply_markup=reply_rec_second_keyboard)
        if len(movies_list) > 1: #Если в списке остались ещё фильмы
            context.user_data['movies_list'] = movies_list[1:]  # Обрезаем первый фильм из movies_list
        else:
            context.user_data.pop('movies_list', None)  # Удаляем movies_list из user_data, если список пустой
#Ждем когда отправится следующий фильм
async def send_next_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'movies_list' in context.user_data:
        await send_movie(update, context)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Список с фильмами по этому названию пустой")