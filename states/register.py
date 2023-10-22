from aiogram.dispatcher.filters.state import State, StatesGroup


class Register(StatesGroup):
    login = State()
    email = State()
    password = State()
