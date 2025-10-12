from aiogram.fsm.state import StatesGroup, State

class Translator(StatesGroup):
    trans = State()
    lang = State()
    text = State()
    select_manually = State()
