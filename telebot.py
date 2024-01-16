import logging
import imdb
import sqlite3
import random
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup, 
    ReplyKeyboardMarkup, 
    ReplyKeyboardRemove, 
    KeyboardButton
)
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    ContextTypes, 
    CommandHandler, 
    MessageHandler, 
    filters
)

#установка уровня логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

#создание экземпляра imdb
ia = imdb.IMDb()

#вынесение повторющегося текста в отдельную переменную
text_help=("1. Напиши название фильма\n2. Я сохраню его\n3. После жми кнопки")

#функция-обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE)  -> int:
    keyboard = [
            [KeyboardButton("Один случайный фильм")],
            [KeyboardButton("Последние 5 добавленных")],
            [KeyboardButton("Выбор жанра")],
        ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_help,\
                                    reply_markup=reply_markup)


#функция- обработчик сохранения фильма
async def savefilm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    film = update.message.text
    movie_title = ia.search_movie(film)
    conn = sqlite3.connect('films.db')
    cursor = conn.cursor()
    try:
        if movie_title:
            movie = ia.get_movie(movie_title[0].movieID)
            cursor.execute('SELECT COUNT(*) FROM films WHERE film = ? AND user_id = ?',\
                           (movie['title'], update.effective_user.id))
            count = cursor.fetchone()[0]


            if count == 0:
                cursor.execute('INSERT INTO films (film, user_id) VALUES (?, ?)',
                               (movie['title'], update.effective_user.id))
                conn.commit()
                await context.bot.send_message(chat_id=update.effective_chat.id, text='Фильм ' +\
                                                movie['title'] + ' ' + str(movie['year']) +' года выпуска сохранен\n\n' +\
                                                      movie['plot outline'])
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text='Фильм ' +\
                                                movie['title'] + ' уже сохранен')
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Фильм не найден")
    except Exception as e:
        conn.rollback()
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Неизвестная ошибка")
    finally:
        conn.close()


#функция выбора из меню
async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
        choice = update.message.text
    
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
        
        if choice == "Выбор жанра":
            """Вывод кнопок в чате после выбора жанра"""
            keyboard = [
                [InlineKeyboardButton("Боевик", callback_data="Боевик")],
                [InlineKeyboardButton("Комедия", callback_data="Комедия")],
                [InlineKeyboardButton("Драма", callback_data="Драма")],
                [InlineKeyboardButton("Триллер", callback_data="Триллер")],
                [InlineKeyboardButton("Фантастика", callback_data="Фантастика")],
                [InlineKeyboardButton("Фэнтези", callback_data="Фэнтези")],
                [InlineKeyboardButton("Мультфильм", callback_data="Мультфильм")],
                [InlineKeyboardButton("Мюзикл", callback_data="Мюзикл")],
                [InlineKeyboardButton("Сажи", callback_data="Семейный")],
                [InlineKeyboardButton("Трагедия", callback_data="Трагедия")],
                [InlineKeyboardButton("Ужасы", callback_data="Ужасы")],
            ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Выберите жанр: ", reply_markup=reply_markup)


if __name__ == '__main__':
    application = ApplicationBuilder().token('5376189132:AAGD207buqYz8yx8xH7EG9BSpQPrqtjW0aM').build()
    
    start_handler = CommandHandler('start', start)
    savefilm_handler = MessageHandler(~filters.Text("Один случайный фильм")\
                                      & ~filters.Text("Последние 5 добавленных")\
                                      & ~filters.Text("Выбор жанра"), savefilm)
    choice_handler = MessageHandler(filters.TEXT, handle_choice)

    application.add_handler(start_handler)
    application.add_handler(savefilm_handler)
    application.add_handler(choice_handler)
    application.add_handler(CallbackQueryHandler(handle_choice))
    

    
    application.run_polling()