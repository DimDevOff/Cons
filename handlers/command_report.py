"""
Файл для обробки репортів
File for processing reports
"""
import logging
from aiogram import types, Router
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest

from config import ADMIN_ID
from utils import sanitize_html

router = Router()

@router.message(Command("report"))
async def report_command1(message: types.Message):
    """
    Коли у відповідь на негарне повідомлення пишуть /report то бот надсилає повідомлення адміну
    з посиланням на повідомлення з репортом і адмін розбирається з негарною людиною
    When /report is written in response to a nasty message, the bot sends a message to the admin
    with a link to the message with the report and the admin deals with the nasty person
    """
    if message.chat.id < 0:
        await message.reply(text="Репорт надішлений! (або рекомендація)")
        user_full_name = sanitize_html(message.from_user.full_name)
        report_text = sanitize_html(message.text)
        await message.bot.send_message(chat_id=ADMIN_ID[0], text=f"Користувач {user_full_name} робить репорт\n"
                                                                 f"url={message.url}\n"
                                                                 f"Текст повідомлення= {report_text}")
    else:
        await message.reply(text="Тут немає людей (хіба ви написали рекомендацію)")
        user_full_name = sanitize_html(message.from_user.full_name)
        report_text = sanitize_html(message.text)
        try:
            await message.bot.send_message(chat_id=ADMIN_ID[0], text=f"Користувач {user_full_name} робить репорт\n"
                                                                     f"url={message.url}\n"
                                                                     f"Текст повідомлення= {report_text}")
        except TelegramBadRequest:
            await message.bot.send_message(chat_id=ADMIN_ID[0], text=f"Користувач {user_full_name} робить репорт\n"
                                                                     f"Приватне повідомлення\n"
                                                                     f"Текст повідомлення= {report_text}")
        except Exception as e:
            logging.error(f"Error sending report from private message: {e}")


@router.message(Command("report", prefix="!"))
async def report_command2(message: types.Message):
    """
    Так само тільки коли пишуть !report
    Similarly, only when writing !report
    """
    if message.chat.id < 0:
        await message.reply(text="Репорт надішлений! (або рекомендація)")
        user_full_name = sanitize_html(message.from_user.full_name)
        report_text = sanitize_html(message.text)
        await message.bot.send_message(chat_id=ADMIN_ID[0], text=f"Користувач {user_full_name} робить репорт\n"
                                                                 f"{message.url}"
                                                                 f"Текст повідомлення= {report_text}")
    else:
        await message.reply(text="Тут немає людей (хіба ви написали рекомендацію)")
        user_full_name = sanitize_html(message.from_user.full_name)
        report_text = sanitize_html(message.text)
        try:
            await message.bot.send_message(chat_id=ADMIN_ID[0], text=f"Користувач {user_full_name} робить репорт\n"
                                                                     f"url={message.url}\n"
                                                                     f"Текст повідомлення= {report_text}")
        except TelegramBadRequest:
            await message.bot.send_message(chat_id=ADMIN_ID[0], text=f"Користувач {user_full_name} робить репорт\n"
                                                                     f"Приватне повідомлення\n"
                                                                     f"Текст повідомлення= {report_text}")
        except Exception as e:
            logging.error(f"Error sending report from private message: {e}")
