from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

ticket_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Добавить билет')]],
    resize_keyboard=True,
)
