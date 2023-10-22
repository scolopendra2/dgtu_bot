from aiogram import types
from aiogram.dispatcher import FSMContext

import models
from keyboards.inlines import ticket_ikb, cancel_ticket_ikb, check_ticket_ikb
from keyboards import webapp_kb
from loader import dp, bot, db
from states import RegisterTicket


@dp.callback_query_handler(text='ticket_cancel', state=RegisterTicket)
async def start_register(call: types.CallbackQuery, state: FSMContext):
    last_message = call.message.message_id
    await bot.delete_message(call.message.chat.id, last_message)
    await state.finish()
    await call.message.answer(
        'Выберите как хотите добавить билет', reply_markup=ticket_ikb
    )


@dp.message_handler(text='Добавить билет')
async def add_ticket(message: types.Message):
    user = (
        db.query(models.User)
        .filter(models.User.tg_user_id == message.from_user.id)
        .first()
    )
    passport = (
        db.query(models.Passport)
        .filter(models.Passport.user_id == user.id)
        .first()
    )
    if passport is None or user is None:
        await message.answer(
            'Чтобы использовать это команду надо пройти регистрацию'
        )
    else:
        await message.answer(
            'Выберите как хотите добавить билет', reply_markup=ticket_ikb
        )


@dp.callback_query_handler(text='register_ticket')
async def register_ticket(call: types.CallbackQuery):
    await call.message.answer(
        'Введите № поезда', reply_markup=cancel_ticket_ikb
    )
    await RegisterTicket.number_train.set()


@dp.message_handler(content_types=['text'], state=RegisterTicket.number_train)
async def set_number_train(message: types.Message, state: FSMContext):
    await state.update_data(number_train=message.text)
    await message.answer('Введите № вагона', reply_markup=cancel_ticket_ikb)
    await RegisterTicket.number_van.set()


@dp.message_handler(content_types=['text'], state=RegisterTicket.number_van)
async def set_number_van(message: types.Message, state: FSMContext):
    await state.update_data(number_van=message.text)
    await message.answer('Введите № места', reply_markup=cancel_ticket_ikb)
    await RegisterTicket.number_place.set()


@dp.message_handler(content_types=['text'], state=RegisterTicket.number_place)
async def set_number_place(message: types.Message, state: FSMContext):
    await state.update_data(number_place=message.text)
    data = await state.get_data()
    number_train = data['number_train']
    number_val = data['number_van']
    number_place = data['number_place']
    await message.answer(
        f'Номер поезда: {number_train}\n'
        f'Номер вагона: {number_val}\n'
        f'Номер места: {number_place}\n'
        f'Всё верно?',
        reply_markup=check_ticket_ikb,
    )
    await RegisterTicket.check.set()


@dp.callback_query_handler(text='yes_ticket', state=RegisterTicket.check)
async def check_ticket(call: types.CallbackQuery, state: FSMContext):
    user = (
        db.query(models.User)
        .filter(models.User.tg_user_id == call.from_user.id)
        .first()
    )
    ticket = models.Ticket()
    ticket.user_id = user.id
    data = await state.get_data()
    ticket.number_train = data['number_train']
    ticket.number_val = data['number_van']
    ticket.number_place = data['number_place']
    db.add(ticket)
    db.commit()
    await call.message.answer('Ваш билет успешно добавлен, теперь '
                              'вы можете ознакомиться с каталогом', reply_markup=webapp_kb)
    await state.finish()
