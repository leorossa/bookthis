#!/usr/bin/env python

from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


start_keyboard = [
    [KeyboardButton("Один случайный фильм")],
    [KeyboardButton("Последние 5 добавленных")],
    [KeyboardButton("Выбор жанра")],
]
reply_start_keyboard = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True)

sim_rec_keyboard = [
        [InlineKeyboardButton("Похожие", callback_data="Похожие")],
        [InlineKeyboardButton("Подробнее", callback_data="Подробнее")],
        ]
reply_sim_rec_keyboard = InlineKeyboardMarkup(sim_rec_keyboard)

text_help = ("1. Напиши название фильма\n2. Я сохраню его\n3. После жми кнопки")