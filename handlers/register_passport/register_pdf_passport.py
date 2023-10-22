import os

from PIL import Image
from aiogram import types
from aiogram.dispatcher import FSMContext
from pdf2image import convert_from_path

from keyboards.inlines import (
    cancel_passport_ikb,
    fio_passport_ikb,
)
from loader import bot, dp
from scripts import get_fio, get_serias, save_pdf
from states import RegisterPassport

poppler_path = r'C:\Users\User\poppler\poppler-23.08.0\Library\bin'


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
