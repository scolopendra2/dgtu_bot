from aiogram.dispatcher.filters.state import State, StatesGroup


class RegisterTicket(StatesGroup):
    number_train = State()
    number_van = State()
    number_place = State()
    photo = State()
    document = State()
    check = State()

    # Поля необходимы, если будет нужно объясню почему
    write_number_train = State()
    write_number_van = State()
    write_number_place = State()
