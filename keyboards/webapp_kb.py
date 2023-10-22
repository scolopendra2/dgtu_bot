from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

webapp_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Добавить билет')],
              [KeyboardButton(text='Каталог', web_app=WebAppInfo(url='https://horvitz.ru/'))]],
    resize_keyboard=True,
)