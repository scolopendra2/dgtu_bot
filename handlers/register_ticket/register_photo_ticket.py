from PIL import Image
from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inlines import (
    cancel_ticket_ikb,
    yes_no_change_ikb,
    change_field,
)
from loader import dp, bot
from scripts import get_ticket_data
from states import RegisterTicket


@dp.callback_query_handler(text='send_photo_ticket')
async def send_photo_ticket(call: types.CallbackQuery):
    await call.message.answer(
        'Отправьте фото билета', reply_markup=cancel_ticket_ikb
    )
    await RegisterTicket.photo.set()


@dp.message_handler(content_types=['photo'], state=RegisterTicket.photo)
async def get_photo_ticket(message: types.Message, state: FSMContext):
    photo = message.photo[-1]

    photo_file = await bot.download_file_by_id(photo.file_id)
    image = Image.open(photo_file)
    await message.answer('Получаю данные с билета⏳')
    data = await get_ticket_data(image)
    train = data['train']
    wagon = data['wagon']
    place = data['place']
    await state.update_data(
        number_train=train, number_van=wagon, number_place=place
    )
    last_message = message.message_id + 1
    await bot.edit_message_text(
        'Данные извлечены успешно✅',
        chat_id=message.chat.id,
        message_id=last_message,
    )

    await message.answer(
        f'Номер поезда:{train}\n'
        f'Номер вагона:{wagon}\n'
        f'Номер места:{place}\nВерно?\n\n'
        f'WARNING: При не правильных данных ваш заказ не будет выполнен',
        reply_markup=yes_no_change_ikb,
    )
    await RegisterTicket.check.set()


@dp.callback_query_handler(text='change_data', state=RegisterTicket.check)
async def change_data(call: types.CallbackQuery):
    await call.message.answer(
        'Выбирете поле которое хотите изменить', reply_markup=change_field
    )
    await RegisterTicket.check.set()


@dp.callback_query_handler(text='change_train', state=RegisterTicket.check)
async def change_train(call: types.CallbackQuery):
    await call.message.answer('Напишите № поезда')
    await RegisterTicket.write_number_train.set()


@dp.message_handler(
    content_types=['text'], state=RegisterTicket.write_number_train
)
async def write_train(message: types.Message, state: FSMContext):
    await state.update_data(number_train=message.text)
    data = await state.get_data()
    train = data['number_train']
    wagon = data['number_van']
    place = data['number_place']
    await message.answer(
        f'Номер поезда: {train}\n'
        f'Номер вагона: {wagon}\n'
        f'Номер места: {place}\nВерно?\n\n'
        f'WARNING: При не правильных данных ваш заказ не будет выполнен',
        reply_markup=yes_no_change_ikb,
    )
    await RegisterTicket.check.set()


@dp.callback_query_handler(text='change_wagon', state=RegisterTicket.check)
async def change_wagon(call: types.CallbackQuery):
    await call.message.answer('Напишите № вагона')
    await RegisterTicket.write_number_van.set()


@dp.message_handler(
    content_types=['text'], state=RegisterTicket.write_number_van
)
async def write_wagon(message: types.Message, state: FSMContext):
    await state.update_data(number_van=message.text)
    data = await state.get_data()
    train = data['number_train']
    wagon = data['number_van']
    place = data['number_place']
    await message.answer(
        f'Номер поезда: {train}\n'
        f'Номер вагона: {wagon}\n'
        f'Номер места: {place}\nВерно?\n\n'
        f'WARNING: При не правильных данных ваш заказ не будет выполнен',
        reply_markup=yes_no_change_ikb,
    )
    await RegisterTicket.check.set()


@dp.callback_query_handler(text='change_place', state=RegisterTicket.check)
async def change_place(call: types.CallbackQuery):
    await call.message.answer('Напишите № места')
    await RegisterTicket.write_number_train.set()


@dp.message_handler(
    content_types=['text'], state=RegisterTicket.write_number_place
)
async def write_place(message: types.Message, state: FSMContext):
    await state.update_data(number_place=message.text)
    data = await state.get_data()
    train = data['number_train']
    wagon = data['number_van']
    place = data['number_place']
    await message.answer(
        f'Номер поезда: {train}\n'
        f'Номер вагона: {wagon}\n'
        f'Номер места: {place}\nВерно?\n\n'
        f'WARNING: При не правильных данных ваш заказ не будет выполнен',
        reply_markup=yes_no_change_ikb,
    )
    await RegisterTicket.check.set()
