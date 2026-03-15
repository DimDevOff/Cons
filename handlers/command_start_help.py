"""Файл для надішлення допомоги"""
from aiogram import types, Router
from aiogram.filters import Command

router = Router()

@router.message(Command("start", "help"))
async def help(message: types.Message):
    """
    Функція для надішлення повідомлення з поясненням

    :param message: для можливості проглянути chat_id, щоб знати куда надіслати повідомлення
    """
    help_message = "КОМАНДИ:\n" \
                   "    /start, /help: Показати це повідомлення\n" \
                   "    /report або !report: Надіслати у відповідь на негарне повідомлення або для рекомендацій " \
                   "автору\n" \
                   "    @save <текст>: Зберегти повідомлення\n" \
                   "    @open: Показати збережене повідомлення\n" \
                   "    /translate: Перекладач\n" \
                   "    /weather: Дізнатися про погоду\n" \
                   "    /weather !: Змінити місто\n" \
                   "    /chat: Почати чат з IvanGPT (альфа версія)\n" \
                   "    /games: Міні ігри\n" \
                   "    /rate: Курс валют вуд НБУ API"
    await message.answer(text=help_message)
