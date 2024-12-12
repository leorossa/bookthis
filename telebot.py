import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    ContextTypes, 
    CommandHandler, 
    MessageHandler, 
    filters
)
from buttons import button_inline
from found_movies import found_films
from movie_saver import savefilm
from oneorfiverandom import random_film
from basekeyboard import reply_start_keyboard, text_help


#установка уровня логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

#функция-обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE)  -> int:
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_help,\
                                    reply_markup=reply_start_keyboard)

#функция-обработчик нажатия на кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await button_inline(update, context)

#Поиск фильма в базе данных tmdb списком
async def foundfilms_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await found_films(update, context)

#Сохранение фильма в базу данных
async def savefilm_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await savefilm(update, context)

#Предложение рандомного фильма из списка сохраненых в базе данных пользователя
async def random_film_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await random_film(update, context)


def main() -> None:
    application = ApplicationBuilder().token('YOUR_BOT_TOCKEN').build()

    foundfilms_handler = MessageHandler(~filters.Text("Один случайный фильм")\
                                      & ~filters.Text("Последние 5 добавленных")\
                                      & ~filters.Text("Выбор жанра"), found_films)


    application.add_handler(CommandHandler('start', start))
    application.add_handler(foundfilms_handler)
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(CallbackQueryHandler(savefilm_handler))
    application.add_handler(MessageHandler(filters.TEXT, callback=random_film_handler))

    application.run_polling()

if __name__ == "__main__":
    main()
