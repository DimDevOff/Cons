"""Файл для надішлення допомоги"""
from aiogram import types, Router

from create_bot import bot

router = Router()

@router.message(commands=["start", "help"])
async def help(message: types.Message):
    """
    Функція для надішлення повідомлення з поясненням

    :param message: для можливості проглянути chat_id, щоб знати куда надіслати повідомлення
    """
    chat_id = message.chat.id
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
    await bot.send_message(chat_id=chat_id, text=help_message)
