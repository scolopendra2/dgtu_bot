from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

passport_ikb = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Отправить фото', callback_data='send_photo_passport'
            )
        ],
        [
            InlineKeyboardButton(
                text='Отправить файл(.pdf)', callback_data='send_file_passport'
            )
        ],
        [
            InlineKeyboardButton(
                text='Ввести вручную', callback_data='register_passport'
            )
        ],
    ],
    resize_keyboard=True,
)

cancel_passport_ikb = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text='Отмена❌', callback_data='passport_cancel')]
    ],
    resize_keyboard=True,
)

fio_passport_ikb = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text='Да✅', callback_data='yes_fio')],
        [
            InlineKeyboardButton(
                text='Изменить вручную🪶', callback_data='change_fio'
            )
        ],
        [
            InlineKeyboardButton(
                text='Отмена❌', callback_data='passport_cancel'
            )
        ],
    ],
    resize_keyboard=True,
)

series_passport_ikb = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text='Да✅', callback_data='yes_series')],
        [
            InlineKeyboardButton(
                text='Изменить вручную🪶', callback_data='change_series'
            )
        ],
        [
            InlineKeyboardButton(
                text='Отмена❌', callback_data='passport_cancel'
            )
        ],
    ],
    resize_keyboard=True,
)

check_ikb = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text='Да✅', callback_data='yes')],
        [InlineKeyboardButton(text='Нет❌', callback_data='no')],
    ],
    resize_keyboard=True,
)
