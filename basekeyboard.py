#!/usr/bin/env python

from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

"""Вариации клавиатур для разных сценариев"""
start_keyboard = [
    [KeyboardButton("Один случайный фильм")],
    [KeyboardButton("Последние 5 добавленных")],
    #[KeyboardButton("Выбор жанра")],
]
reply_start_keyboard = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=False)

save_pon_keyboard = [
        [InlineKeyboardButton("Сохранить", callback_data="Сохранить")],
        [InlineKeyboardButton("Рекомендации", callback_data="Рекомендации")],
        [InlineKeyboardButton("Понятно", callback_data="Понятно")],
        ]
reply_save_pon_keyboard = InlineKeyboardMarkup(save_pon_keyboard)

rec_second_keyboard = [
        [InlineKeyboardButton("Сохранить", callback_data="Сохранить")],
        [InlineKeyboardButton("Рекомендации", callback_data="Рекомендации")],
        [InlineKeyboardButton("Далее", callback_data="Далее")],
]
reply_rec_second_keyboard = InlineKeyboardMarkup(rec_second_keyboard)

pon_keyboard = [
        [InlineKeyboardButton("Понятно", callback_data="Понятно")],
]
reply_pon_keyboard = InlineKeyboardMarkup(pon_keyboard)

details_keyboard = [
        [InlineKeyboardButton("Подробнее", callback_data="Подробнее")],
        [InlineKeyboardButton("Понятно", callback_data="Понятно")],
]
reply_details_keyboard = InlineKeyboardMarkup(details_keyboard)

"""Помошник для выдачи информации если пользователь не ввел название фильма"""
text_help = (
    "1. Напиши мне название фильма\n"
    "2. Я найду все фильмы связанные с этим названием\n"
    "3. Похожие - поиск фильмов схожих по сюжету, жанрам и тп.\n"
    "4. Далее - следующий фильм из списка.\n"
    "5. Сохранить - сохраняет текущий выбранный фильм.\n"
    "6. Подробнее - показывает подробную информацию."
)

"""
Помошник для обработки жанров по id
genre_data = {
        {"id":28,"name":"Экшн"},
        {"id":12,"name":"Приключения"},
        {"id":16,"name":"Анимация"},
        {"id":35,"name":"Комедия"},
        {"id":80,"name":"Преступления"},
        {"id":99,"name":"Документальный"},
        {"id":18,"name":"Драма"},
        {"id":10751,"name":"Семейный"},
        {"id":14,"name":"Фантастика"},
        {"id":36,"name":"Исторический"},
        {"id":27,"name":"Ужасы"},
        {"id":10402,"name":"Музыкальный"},
        {"id":9648,"name":"Мистика"},
        {"id":10749,"name":"Романтика"},
        {"id":878,"name":"Научная фантастика"},
        {"id":10770,"name":"Телевизионный"},
        {"id":53,"name":"Триллер"},
        {"id":10752,"name":"Военный"},
        {"id":37,"name":"Вестерн"}
}
genre_id_to_name = {genre['id']: genre['name'] for genre in genre_data}
"""