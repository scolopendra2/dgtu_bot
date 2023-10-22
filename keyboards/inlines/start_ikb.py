from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_ikb = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text='Регистрация', callback_data='register')]
    ],
    resize_keyboard=True,
)

cancel_ikb = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text='Отмена❌', callback_data='register_cancel')]
    ],
    resize_keyboard=True,
)
