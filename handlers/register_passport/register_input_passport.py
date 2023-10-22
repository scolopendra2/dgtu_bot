from aiogram import types
from aiogram.dispatcher import FSMContext

import models
from keyboards.inlines import cancel_passport_ikb, check_ikb, passport_ikb
from loader import bot, db, dp
from states import RegisterPassport


@dp.callback_query_handler(text='register_passport')
async def register_passport(call: types.CallbackQuery):
    user = (
        db.query(models.User)
        .filter(models.User.tg_user_id == call.from_user.id)
        .first()
    )
    passport = (
        db.query(models.Passport)
        .filter(models.Passport.user_id == user.id)
        .first()
    )
    if passport is None:
        await call.message.answer(
            'Введите своё ФИО', reply_markup=cancel_passport_ikb
        )
        await RegisterPassport.full_name.set()
    else:
        await call.message.answer('Вы уже зарегистрировали паспортные данные')


@dp.message_handler(content_types=['text'], state=RegisterPassport.full_name)
async def reg_fio(message: types.Message, state: FSMContext):
    text = message.text
    if len(text.split()) != 3:
        await message.answer(
            'Данные введены не корректно попробуйте снова',
            reply_markup=cancel_passport_ikb,
        )
    else:
        await state.update_data(
            full_name=' '.join(
                list(map(lambda x: x.lower().capitalize(), text.split()))
            )
        )
        await message.answer(
            'Введите свою серию и номер паспорта',
            reply_markup=cancel_passport_ikb,
        )
        await RegisterPassport.series_and_number.set()


@dp.message_handler(
    content_types=['text'], state=RegisterPassport.series_and_number
)
async def reg_series(message: types.Message, state: FSMContext):
    text = ''.join(message.text.split())
    if not text.isdigit():
        await message.answer(
            'Серия и номер должны состоять только из цифр',
            reply_markup=cancel_passport_ikb,
        )
    elif len(text) != 10:
        await message.answer(
            'Серия и номер должны состоять только из 10 цифр',
            reply_markup=cancel_passport_ikb,
        )
    else:
        data = await state.get_data()
        fullname = data['full_name']
        series = message.text
        await state.update_data(series_and_number=series)
        await message.answer(
            f'ФИО: {fullname}\n' f'Серия и номер: {series}\n' f'Верно?',
            reply_markup=check_ikb,
        )
        await RegisterPassport.check_data.set()


@dp.callback_query_handler(text='yes', state=RegisterPassport.check_data)
async def check_yes(call: types.CallbackQuery, state: FSMContext):
    user = (
        db.query(models.User)
        .filter(models.User.tg_user_id == call.from_user.id)
        .first()
    )
    passport = models.Passport()
    data = await state.get_data()
    passport.series_and_number = data['series_and_number']
    passport.user_id = user.id
    passport.full_name = data['full_name']
    db.add(passport)
    db.commit()
    await call.message.answer('Паспортные данные успешно зарегистрированы')
    await state.finish()


@dp.callback_query_handler(text='no', state=RegisterPassport.check_data)
async def check_no(call: types.CallbackQuery, state: FSMContext):
    last_message = call.message.message_id
    await bot.delete_message(call.message.chat.id, last_message)
    await state.finish()
    await call.message.answer(
        'Для продолжения мне нужны ваши паспортные данные',
        reply_markup=passport_ikb,
    )
