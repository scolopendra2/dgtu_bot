from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ticket_ikb = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Отправить фото билета', callback_data='send_photo_ticket'
            )
        ],
        [
            InlineKeyboardButton(
                text='Отправить файл билета(.pdf)',
                callback_data='send_file_ticket',
            )
        ],
        [
            InlineKeyboardButton(
                text='Ввести вручную данные билета',
                callback_data='register_ticket',
            )
        ],
    ],
    resize_keyboard=True,
)

cancel_ticket_ikb = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text='Отмена❌', callback_data='ticket_cancel')]
    ],
    resize_keyboard=True,
)

check_ticket_ikb = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text='Да✅', callback_data='yes_ticket')],
        [InlineKeyboardButton(text='Нет❌', callback_data='ticket_cancel')],
    ],
    resize_keyboard=True,
)

yes_no_change_ikb = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text='Да✅', callback_data='yes_ticket')],
        [
            InlineKeyboardButton(
                text='Изменить поля🪶', callback_data='change_data'
            )
        ],
        [InlineKeyboardButton(text='Нет❌', callback_data='ticket_cancel')],
    ],
    resize_keyboard=True,
)

change_field = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text='№ Поезда', callback_data='change_train')],
        [InlineKeyboardButton(text='№ Вагона', callback_data='change_wagon')],
        [InlineKeyboardButton(text='№ Места', callback_data='change_place')],
    ],
    resize_keyboard=True,
)
