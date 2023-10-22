from loader import dp, db, bot
from aiogram import types
import json
import models


@dp.message_handler(content_types="web_app_data")
async def get_data(webAppMes: types.WebAppData):
    all_sum = 0
    all_string = ''
    chat = webAppMes.chat.id
    data = webAppMes.web_app_data.data
    data = json.loads(data)
    for k, v in data.items():
        product = db.query(models.Product).filter(models.Product.name == k).first()
        price = product.price
        all_sum += price * v
        all_string += f'{k}: {v}\n'
    all_string += (f'---------------------------------\nИтого: {all_sum}р.\n'
                   f'---------------------------------\n')
    user = db.query(models.User).filter(models.User.tg_user_id == chat).first()
    ticket = db.query(models.Ticket).filter(models.Ticket.user_id == user.id).first()
    wagon = ticket.number_val
    place = ticket.number_place
    all_string += (f'Доставка в:\n'
                   f'Вагон: {wagon}\n'
                   f'Место: {place}\n'
                   f'Доставят в ближайшее время')
    await bot.send_message(chat_id=chat, text=all_string)


