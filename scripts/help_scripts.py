import re

import pytesseract

from loader import bot

pytesseract.pytesseract.tesseract_cmd = (
    r'C:\Program Files\Tesseract-OCR\tesseract.exe'
)


async def save_pdf(message):
    file_id = message.document.file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path

    file = await bot.download_file(file_path)

    with open(file_path, 'wb') as f:
        f.write(file.read())
    file.close()
    return file_path


async def get_serias(img):
    img = img.rotate(-270, expand=True)
    new_height = int(img.height * 0.15)
    img = img.crop((0, 0, img.width, new_height))
    img = img.resize((1580, new_height))
    text = ''.join(pytesseract.image_to_string(img).split('\n'))
    return ''.join(re.findall(r'[0-9]', text)[:10])


def delete_symbols(text):
    return re.sub('[^a-zA-Zа-яА-Я \n]', '', text)


async def get_fio(img):
    img = img.crop((0, img.height // 2 + 2, img.width, img.height))
    text = delete_symbols(pytesseract.image_to_string(img, lang='rus')).split(
        '\n'
    )
    text = list(filter(lambda x: x.strip() != '', text))

    fio = []
    for i in text:
        match = re.search(r'^\s?(?:[а-я]*\s*)([А-Я]{5,20})\s?[а-я]*$', i)
        if match:
            fio.append(match.group(1))
    return ' '.join(fio)


async def get_ticket_data(img):
    text = pytesseract.image_to_string(img, lang='rus')

    train = re.search(r'[0-9]{3}[A-ZА-Я] ', text, re.IGNORECASE)
    wagon = re.search(r' [0-9]{2} ', text, re.IGNORECASE)
    place = re.search(r' [0-9]{3} ', text, re.IGNORECASE)

    return {
        'train': train.group()
        if train is not None
        else 'Не удалось распознать номер поезда',
        'wagon': wagon.group()
        if wagon is not None
        else 'Не удалось распознать номер вагона',
        'place': place.group()
        if place is not None
        else 'Не удалось распознать номер места',
    }
