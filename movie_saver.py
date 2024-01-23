#!/usr/bin/env python

import sqlite3
from telegram import Update
from telegram.ext import ContextTypes


async def savefilm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    film = context.user_data["film"] #Получаем название фильма из user_data после нажатия кнопки Сохранить
    conn = sqlite3.connect('films.db') #Подключаемся к базе данных
    cursor = conn.cursor() #Создаем курсор

    try: #Пытаемся сохранить фильм
        if film: #Если название фильма не пустое
            """Смотрим записи в таблице films, по пользователю и списку фильмов"""
            cursor.execute('SELECT COUNT(*) FROM films WHERE user_id = ? AND film = ?',\
                            (update.effective_user.id, film))
            count = cursor.fetchone()[0]  #Получаем количество записей

            if count == 0: #Если записи не существует
                """Сохраняем фильм в таблицу films"""
                cursor.execute('INSERT INTO films (user_id,film) VALUES (?, ?)',
                                (update.effective_user.id, film))
                conn.commit() #Сохраняем изменения
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Фильм сохранен")
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Фильм уже сохранен")
        
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Фильм не найден")
    except Exception as e:
        conn.rollback() #Откатываемся в случае ошибки
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Неизвестная ошибка при сохранении фильма\
                                        Посмотри в movie_saver")
    finally:
        conn.close() #Закрываем соединение с базой данных
        