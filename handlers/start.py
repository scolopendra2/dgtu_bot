from aiogram import types

from loader import dp


@dp.message_handler(text='/start')
async def start(message: types.Message):
    await message.answer(
        'Привет я бот от команды NT, создан для покупки еды '
        'в поездке не двигаясь с места, для продолжения нужно пройти '
        'регистрацию.\n'
        'Как мне вас называть?'
    )
