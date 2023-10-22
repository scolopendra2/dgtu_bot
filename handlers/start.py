from aiogram import types
from aiogram.dispatcher import FSMContext

import models
from keyboards.inlines import cancel_ikb, passport_ikb, start_ikb
from loader import bot, db, dp
from states import Register


@dp.message_handler(text='/start')
async def start(message: types.Message):
    await message.answer(
        'Привет я бот от команды NT, создан для покупки еды '
        'в поездке не двигаясь с места, для продолжения необходимо '
        'зарегистрироваться',
        reply_markup=start_ikb,
    )


@dp.callback_query_handler(text='register')
async def start_register(call: types.CallbackQuery):
    if (
        db.query(models.User)
        .filter(models.User.tg_user_id == call.from_user.id)
        .first()
        is None
    ):
        await call.message.answer('Логин:', reply_markup=cancel_ikb)
        await Register.login.set()
    else:
        await call.message.answer('Вы уже зарегистрированы в боте')


@dp.message_handler(state=Register.login)
async def check_number(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer('Email:', reply_markup=cancel_ikb)
    await Register.email.set()


@dp.message_handler(state=Register.email)
async def check_number(message: types.Message, state: FSMContext):
    if '@' not in message.text:
        await message.answer(
            f'Символа `@` нет в {message.text},' f' попробуйте снова:',
            reply_markup=cancel_ikb,
        )
        await Register.email.set()
    else:
        await state.update_data(email=message.text)
        await message.answer('Пароль:', reply_markup=cancel_ikb)
        await Register.password.set()


@dp.message_handler(state=Register.password)
async def check_number(message: types.Message, state: FSMContext):
    user = models.User()
    user.tg_user_id = message.from_user.id
    data = await state.get_data()
    login = data['login']
    email = data['email']
    user.user_login = login
    user.user_email = email
    user.user_password = message.text
    db.add(user)
    db.commit()
    await message.answer(
        'Для продолжения мне нужны ваши паспортные данные',
        reply_markup=passport_ikb,
    )
    await state.finish()


@dp.callback_query_handler(text='register_cancel', state=Register)
async def start_register(call: types.CallbackQuery, state: FSMContext):
    last_message = call.message.message_id
    await bot.delete_message(call.message.chat.id, last_message)
    await state.finish()
    await call.message.answer(
        'Привет я бот от команды NT, создан для покупки еды '
        'в поездке не двигаясь с места, для продолжения необходимо '
        'зарегистрироваться',
        reply_markup=start_ikb,
    )
