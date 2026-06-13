from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    first_name = State()
    last_name = State()
    patronymic = State()
    birth_date = State()
    grade = State()
    location = State()
    phone = State()
