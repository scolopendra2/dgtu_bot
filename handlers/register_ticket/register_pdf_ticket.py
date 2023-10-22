import os

from PIL import Image
from aiogram import types
from aiogram.dispatcher import FSMContext
from pdf2image import convert_from_path

from keyboards.inlines import yes_no_change_ikb, cancel_ticket_ikb
from loader import dp, bot
from scripts import get_ticket_data
from scripts import save_pdf
from states import RegisterTicket

poppler_path = r'C:\Users\User\poppler\poppler-23.08.0\Library\bin'


@dp.callback_query_handler(text='send_file_ticket')
async def get_pdf(call: types.CallbackQuery):
    await call.message.answer(
        'Отправьте билет в pdf формате', reply_markup=cancel_ticket_ikb
    )
    await RegisterTicket.document.set()


@dp.message_handler(content_types=['document'], state=RegisterTicket.document)
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
            'Получаю данные с билета⏳',
            chat_id=message.chat.id,
            message_id=last_message,
        )
        data = await get_ticket_data(img)
        train = data['train']
        wagon = data['wagon']
        place = data['place']
        await state.update_data(
            number_train=train, number_van=wagon, number_place=place
        )
        img.close()
        os.remove(path_image)
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
