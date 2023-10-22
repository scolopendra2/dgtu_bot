from aiogram.dispatcher.filters.state import State, StatesGroup


class RegisterPassport(StatesGroup):
    full_name = State()
    series_and_number = State()
    photo = State()
    document = State()
    write_full_name = (
        State()
    )  # доп поля чтобы не сбить handler в ручной записи
    write_series = State()
    check_data = State()
