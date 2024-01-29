from telegram import Update
from telegram.ext import ContextTypes
from tmdbv3api import TMDb, Movie

from basekeyboard import reply_rec_second_keyboard, reply_save_pon_keyboard

#Подключаемся к базе imdb
tmdb = TMDb()
tmdb.api_key = "95982a3f170dcc7789a72455024860b2"
tmdb.language = 'ru'
movie = Movie()


#Берем название фильма из описания для постера фильма query.message.caption
async def found_films(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Ищем фильмы по списку связанных с этим названием от пользователя"""
    context.user_data.clear()  # Очищаем весь контекст для нового поиска
    films = update.message.text
    search_films = movie.search(films)  # Возвращаем список с похожими названиями
    context.user_data['search_films'] = search_films  # Передаем в контекст для дальнейшего использования по источнику
    await create_film_list(update, context)  # Отправляем в создание списка фильмов


async def send_recomendation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Создание нового списка рекомендованных фильмов после нажатия Рекомендации"""
    if 'id' in context.user_data:
        film_id = context.user_data['id']
        context.user_data.clear()
    recommendations = movie.recommendations(movie_id=film_id) #Поиск рекомендованных фильмов с ограничением на 1 страницу
    context.user_data['rec_list'] = recommendations
    await create_film_list(update, context)


async def send_overwiev(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправка фильма после рандомного выбора от пользователя"""
    if 'overview_movies' in context.user_data:
        films = context.user_data['overview_movies']
        context.user_data.clear()
    overwiev_films = movie.search(films)
    context.user_data['overwiev_list'] = overwiev_films
    await create_film_list(update, context)


async def create_film_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Создание итогового списка для передачи пользователю"""
    default_popularity = 0
    if 'rec_list' in context.user_data:
        films = context.user_data['rec_list']
    elif 'overwiev_list' in context.user_data:
        films = context.user_data['overwiev_list']
    elif 'search_films' in context.user_data:
        films = context.user_data['search_films']  #Получаем список из введенного сообщения от пользователя
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Не удалось создать список с фильмами")
    for f in films:
        if not hasattr(f, 'popularity') or not f.popularity:
            f.popularity = 0
        if not hasattr(f, 'release_date') or not f.release_date:
            f.release_date = "В производстве" #Добавляем дату релиза если ее нет
        if not hasattr(f, 'poster_path') or not f.poster_path:
            f.poster_path = 'https://www.hi-fi.ru/upload/medialibrary/5c8/5c87214a87d47f09d36daa4787d65291.jpg'
        else:
            f.poster_path = 'https://image.tmdb.org/t/p/w500' + f.poster_path
    films = sorted(films, key=lambda x: x.popularity, reverse=True) #Сортируем по популярности от большего к меньшему
    context.user_data['main_list'] = films  #Передаем в контекст для отправки пользователю
    await send_movie(update, context)



async def send_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправка фильма пользователю, через расшифровку id фильма"""
    movies_list = context.user_data['main_list']
    
    if movies_list: #Если список не пустой
        movies = movies_list[0] #Берем первый элемент
        reply_markup = reply_rec_second_keyboard if len(movies_list) > 0 else reply_save_pon_keyboard #Выбираем клавиатуру
        context.user_data['id'] = movies.id 
        context.user_data['title'] = movies.title
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo= movies.poster_path,\
                                        caption=movies.title + '\n\n' + movies.overview + '\n\n' + 'Рейтинг: '\
                                            + str(movies.vote_average) + ' | Дата релиза: ' + str(movies.release_date),\
                                                reply_markup=reply_markup)

        if len(movies_list) > 1: #Если в списке остались ещё фильмы
            context.user_data['main_list'] = movies_list[1:]  # Обрезаем первый фильм
        else:
            context.user_data.pop('main_list', None)  # Удаляем movies_list из user_data, если список пустой

#Ждем когда отправится следующий фильм
async def send_next_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'main_list' in context.user_data:
        await send_movie(update, context)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Список с фильмами по этому названию пустой")