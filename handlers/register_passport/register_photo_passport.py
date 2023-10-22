import os

from PIL import Image
from aiogram import types
from aiogram.dispatcher import FSMContext
from pdf2image import convert_from_path
from scripts import get_fio, get_serias, save_pdf
import models
from keyboards.inlines import (
    cancel_passport_ikb,
    fio_passport_ikb,
    passport_ikb,
    series_passport_ikb,
)
from loader import bot, db, dp
from states import RegisterPassport

poppler_path = r'C:\Users\User\poppler\poppler-23.08.0\Library\bin'


@dp.callback_query_handler(text='send_file_passport')
async def file_passport(call: types.CallbackQuery):
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
            'Пришлите документ с паспортом формата .pdf',
            reply_markup=cancel_passport_ikb,
        )
        await RegisterPassport.document.set()
    else:
        await call.message.answer('Вы уже зарегистрировали паспортные данные')


@dp.message_handler(
    content_types=['document'], state=RegisterPassport.document
)
async def get_pdf(message: types.Message, state: FSMContext):
    document = message.document
    if document.mime_type == 'application/pdf':
        await message.answer('Преобразую pdf в картинку...⏳')
        path = await save_pdf(message)
        images = convert_from_path(path, poppler_path=poppler_path)
        path_image = f'documents/{message.from_user.id}.jpg'
        images[0].save(path_image)
        img = Image.open(path_image)
        os.remove(path)
        last_message = message.message_id + 1
        await bot.edit_message_text(
            'Получаю ваше ФИО⏳',
            chat_id=message.chat.id,
            message_id=last_message,
        )
        fullname = await get_fio(img)
        fullname = ' '.join(
            list(map(lambda x: x.lower().capitalize(), fullname.split()))
        )
        await state.update_data(full_name=fullname)
        last_message = message.message_id + 1
        await bot.edit_message_text(
            'Получаю серию и номер паспорта⏳',
            chat_id=message.chat.id,
            message_id=last_message,
        )
        series_and_number = await get_serias(img)
        series_and_number = (
            series_and_number[0:2]
            + ' '
            + series_and_number[2:4]
            + ' '
            + series_and_number[4:]
        )
        await state.update_data(series_and_number=series_and_number)
        img.close()
        os.remove(path_image)
        last_message = message.message_id + 1
        await bot.edit_message_text(
            'Данные извлечены успешно✅',
            chat_id=message.chat.id,
            message_id=last_message,
        )
        await message.answer(
            f'{fullname} - Ваше ФИО?', reply_markup=fio_passport_ikb
        )
        await RegisterPassport.full_name.set()
    else:
        await message.answer(
            'Пожалуйста, отправьте файл в формате PDF.',
            reply_markup=cancel_passport_ikb,
        )


@dp.callback_query_handler(text='passport_cancel', state=RegisterPassport)
async def start_register(call: types.CallbackQuery, state: FSMContext):
    last_message = call.message.message_id
    await bot.delete_message(call.message.chat.id, last_message)
    await state.finish()
    await call.message.answer(
        'Для продолжения мне нужны ваши паспортные данные',
        reply_markup=passport_ikb,
    )


@dp.callback_query_handler(text='send_photo_passport')
async def get_photo_passport(call: types.CallbackQuery):
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
            'Пришлите фото паспорта', reply_markup=cancel_passport_ikb
        )
        await RegisterPassport.photo.set()
    else:
        await call.message.answer('Вы уже зарегистрировали паспортные данные')


@dp.message_handler(content_types=['photo'], state=RegisterPassport.photo)
async def get_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1]

    photo_file = await bot.download_file_by_id(photo.file_id)
    image = Image.open(photo_file)

    await message.answer('Получаю ваше ФИО⏳')
    fullname = await get_fio(image)
    fullname = ' '.join(
        list(map(lambda x: x.lower().capitalize(), fullname.split()))
    )
    await state.update_data(full_name=fullname)
    last_message = message.message_id + 1
    await bot.edit_message_text(
        'Получаю серию и номер паспорта⏳',
        chat_id=message.chat.id,
        message_id=last_message,
    )
    series_and_number = await get_serias(image)
    series_and_number = (
        series_and_number[0:2]
        + ' '
        + series_and_number[2:4]
        + ' '
        + series_and_number[4:]
    )
    await state.update_data(series_and_number=series_and_number)
    last_message = message.message_id + 1
    await bot.edit_message_text(
        'Данные извлечены успешно✅',
        chat_id=message.chat.id,
        message_id=last_message,
    )
    await message.answer(
        f'{fullname} - Ваше ФИО?', reply_markup=fio_passport_ikb
    )
    await RegisterPassport.full_name.set()


@dp.callback_query_handler(text='yes_fio', state=RegisterPassport.full_name)
async def yes_fio(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    series = data['series_and_number']
    await call.message.answer(
        f'{series} - Ваши серия и номер?', reply_markup=series_passport_ikb
    )
    await RegisterPassport.series_and_number.set()


@dp.callback_query_handler(text='change_fio', state=RegisterPassport.full_name)
async def change_fio(call: types.CallbackQuery):
    await call.message.answer(
        'Напишите ваше ФИО', reply_markup=cancel_passport_ikb
    )
    await RegisterPassport.write_full_name.set()


@dp.message_handler(
    content_types=['text'], state=RegisterPassport.write_full_name
)
async def write_full_name(message: types.Message, state: FSMContext):
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

        data = await state.get_data()
        series = data['series_and_number']
        await message.answer(
            f'{series} - Ваши серия и номер?', reply_markup=series_passport_ikb
        )
        await RegisterPassport.series_and_number.set()


@dp.callback_query_handler(
    text='yes_series', state=RegisterPassport.series_and_number
)
async def yes_series(call: types.CallbackQuery, state: FSMContext):
    user = (
        db.query(models.User)
        .filter(models.User.tg_user_id == call.from_user.id)
        .first()
    )
    passport = models.Passport()
    data = await state.get_data()
    passport.user_id = user.id
    passport.full_name = data['full_name']
    passport.series_and_number = data['series_and_number']
    db.add(passport)
    db.commit()
    await call.message.answer('Паспортные данные успешно зарегистрированы')
    await state.finish()


@dp.callback_query_handler(
    text='change_series', state=RegisterPassport.series_and_number
)
async def change_series(call: types.CallbackQuery):
    await call.message.answer(
        'Напишите свою серию и номер паспорта',
        reply_markup=cancel_passport_ikb,
    )
    await RegisterPassport.write_series.set()


@dp.message_handler(
    content_types=['text'], state=RegisterPassport.write_series
)
async def write_series(message: types.Message, state: FSMContext):
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
        user = (
            db.query(models.User)
            .filter(models.User.tg_user_id == message.from_user.id)
            .first()
        )
        passport = models.Passport()
        passport.series_and_number = message.text
        data = await state.get_data()
        passport.user_id = user.id
        passport.full_name = data['full_name']
        db.add(passport)
        db.commit()
        await message.answer('Паспортные данные успешно зарегистрированы')
        await state.finish()
