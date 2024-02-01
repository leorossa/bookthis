#!/usr/bin/env python

from telegram import Update
from telegram.ext import ContextTypes

from movie_saver import savefilm
from found_movies import(
    send_recomendation,
    send_overwiev,
    send_next_movie,
    send_popular,
    send_youtube
)


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
    
    elif query.data == "Похожее":
        await send_recomendation(update, context)
        await update.callback_query.message.delete()

    elif query.data == "Закрыть":
        await update.callback_query.message.delete()
    
    elif query.data == "Подробнее":
        await send_overwiev(update, context)
        await update.callback_query.message.delete()

    elif query.data == "Назад":
        await send_back(update, context)
        await update.callback_query.message.delete()
    
    elif query.data == "Что посмотреть?":
        await send_popular(update, context)

    elif query.data == "Ютюбчик":
        await send_youtube(update, context)