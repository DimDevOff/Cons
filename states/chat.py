from aiogram.fsm.state import StatesGroup, State


class Chat(StatesGroup):
    warning_and_start_chat = State()
