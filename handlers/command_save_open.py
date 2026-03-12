"""
    Файловий провідник
    File Explorer

    Що він робить?
    What is he doing?

    1.Може показати всі файли в папці для цього треба написати боту таку команду @dir view або @dir <ім'я папки>

    1.You can show all the files in the folder, for this you need to write the following command to the bot: @dir view
     or @dir <folder name>

    2.Може показати всі зображення в папці media/image з параметром img або txt

    2.Can show all images in media/image folder with img or txt option

    3.Може фільтрувати повідомлення (для фільтрації треба написати в config.py слова яких не має бути в повідомленнях)

    3.Can filter messages (for filtering, you need to write in config.py words that should not be in messages)
"""
import json
import logging

from aiogram import types, Router
from aiogram.filters import Command

import config as cnf

router = Router()

@router.message(lambda message: message.text.startswith('@save') or message.text.startswith('@open'))
async def save_open(message: types.Message):
    """
    Коли людина пише @save {текст}
    то бот бере це повідомлення вирізає з нього "@save ",
    і зберігає його в saves_texts.json де за ключ виступає ID користувача.
    А значення це збережений текст.
    І коли людина пише @open то файл saves_texts.json,
    зчитується і по ключу (тобто ID  користувача) береться збережений текст

    When a person writes @save {text},
    the bot takes this message, cuts out "@save",
    from it and saves it in saves_texts.json where the key is the user ID,
    and the value is the saved text.
    And when a person writes @open, the saves_texts.json,
    file is read and the saved text is taken based on the key (that is, the user ID)
    """
    
    import os

    chat_id = message.chat.id
    user_id = str(message.from_user.id)
    message_text = message.text.split()

    json_dir = "json"
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)
    saves_file_path = os.path.join(json_dir, "saves_texts.json")

    match message_text:
        case ["@open"]:
            try:
                with open(saves_file_path, "r", encoding="utf-8") as f:
                    saved_data = json.load(f)
                    if user_id in saved_data:
                        await message.reply(text=saved_data[user_id])
                    else:
                        await message.reply(text="Ви ще нічого не зберегли.")
            except FileNotFoundError:
                await message.reply(text="Ви ще нічого не зберегли.")
            except Exception as e:
                logging.error(f"Error reading {saves_file_path}: {e}")
                await message.reply(text="Сталась помилка!")

        case ["@save", *text]:
            # збереження тексту у save_text
            save_text = " ".join(text)

            # Спробувати прочитати файл saves_texts
            try:
                with open(saves_file_path, "r", encoding="utf-8") as f:
                    saves_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                saves_data = {}

            saves_data[user_id] = save_text

            try:
                with open(saves_file_path, "w", encoding="utf-8") as f:
                    json.dump(saves_data, f, ensure_ascii=False, indent=4)
                await message.reply(text="Текст збережено!")
            except Exception as e:
                logging.error(f"Error writing to {saves_file_path}: {e}")
                await message.reply(text="Не вдалося зберегти текст.")
    message_text = message.text.lower().split()
    for word in cnf.WORDS:
        if word in message_text:
            await message.delete()
    msg = f"https://t.me/{message.from_user.username}, {message.from_user.language_code}, {message.from_user.id}," \
          f" @{message.from_user.username}, {message.from_user.full_name}, chat id={chat_id} => {message.text}"
    logging.info(msg=msg)
