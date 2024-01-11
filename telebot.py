import logging
import imdb
import sqlite3
import random
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

#установка уровня логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

#создание экземпляра imdb
ia = imdb.IMDb()

#функция-обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Меню:" + "\n/start - запуск бота и меню" +\
                                    "\nНапиши мне название фильма, я поищу такой его в базе" +\
                                          "\n/getfilms - получить сохраненные фильмы")


#функция- обработчик сохранения фильма
async def savefilm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    film = update.message.text
    movie_title = ia.search_movie(film)
    conn = sqlite3.connect('films.db')
    cursor = conn.cursor()
    try:
        if movie_title:
            movie = ia.get_movie(movie_title[0].movieID)
            cursor.execute('INSERT INTO films (film, user_id) VALUES (?, ?)',\
                            (movie['title'], update.effective_user.id))
            conn.commit()
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Фильм ' + movie['title'] +\
                                            ' ' + str(movie['year']) + ' года выпуска' + ' сохранен' +\
                                            '\n/start - вернуться в меню')
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Фильм не найден" +\
                                            "\n/start - вернуться в меню")
    except Exception as e:
        conn.rollback()
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Неизвестная ошибка" +\
                                            "\n/start - вернуться в меню")
    finally:
        conn.close()


#функция- обработчик команды /getfilms для получения списка сохраненных фильмов
async def getfilms(update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [KeyboardButton("Показать 1 случайный фильм")],
            [KeyboardButton("Показать последние 5 добавленных фильмов")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Выберите действие:", reply_markup=reply_markup)

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
        choice = update.message.text
    
        if choice == "Показать 1 случайный фильм":
            conn = sqlite3.connect('films.db')
            cursor = conn.cursor()
            cursor.execute('SELECT film FROM films WHERE user_id = ?', (update.effective_user.id,))
            films = cursor.fetchall()
            conn.close()
        
            if not films:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="У вас нет сохраненных фильмов")
            else:
                random_film = random.choice(films)
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Случайный фильм: {random_film[0]}")
    
        elif choice == "Показать последние 5 добавленных фильмов":
            conn = sqlite3.connect('films.db')
            cursor = conn.cursor()
            cursor.execute('SELECT film FROM films WHERE user_id = ? ORDER BY id DESC LIMIT 5', (update.effective_user.id,))
            films = cursor.fetchall()
            conn.close()
        
            if not films:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="У вас нет сохраненных фильмов")
            else:
                films_list = "\n".join([film[0] for film in films])
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Последние 5 добавленных фильмов:\n{films_list}")


if __name__ == '__main__':
    application = ApplicationBuilder().token('5376189132:AAGD207buqYz8yx8xH7EG9BSpQPrqtjW0aM').build()
    
    start_handler = CommandHandler('start', start)
    getfilms_handler = CommandHandler('getfilms', getfilms)
    savefilm_handler = MessageHandler(filters.TEXT, savefilm)

    application.add_handler(start_handler)
    application.add_handler(getfilms_handler)
    application.add_handler(savefilm_handler)

    
    application.run_polling()