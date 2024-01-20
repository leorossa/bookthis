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
from movie_saver import savefilm
from recomendation import button
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

#Сохранение фильма в базу данных
async def savefilm_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await savefilm(update, context)

#Предложение рандомного фильма из списка сохраненых в базе данных пользователя
async def random_film_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await random_film(update, context)

#Обработчик кнопок после добавления 
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await button(update, context)


def main() -> None:
    application = ApplicationBuilder().token('5376189132:AAGD207buqYz8yx8xH7EG9BSpQPrqtjW0aM').build()
    
    savefilm_handler = MessageHandler(~filters.Text("Один случайный фильм")\
                                      & ~filters.Text("Последние 5 добавленных")\
                                      & ~filters.Text("Выбор жанра"), savefilm)

    application.add_handler(CommandHandler('start', start))
    application.add_handler(savefilm_handler)
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT, callback=random_film_handler))
    

    
    application.run_polling()

if __name__ == "__main__":
    main()