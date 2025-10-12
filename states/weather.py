from aiogram.fsm.state import StatesGroup, State

class Weather(StatesGroup):
    city = State()
