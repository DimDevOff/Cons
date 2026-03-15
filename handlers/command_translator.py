"""
Файл для перекладу
File for translation
"""
import logging
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
import translators.server as tss

from states.translator import Translator as ts
from keyboards.transtalor import *

router = Router()

@router.message(Command("translate"))
async def translation(message: types.Message, state: FSMContext):
    """
    Функція для запуску перекладача
    Function to start the translator
    """
    await state.set_state(ts.trans)
    await message.answer(text="Ви який перекладач хочете використати?", reply_markup=choosing_translator)


@router.callback_query(ts.trans)
async def used_translator(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Статус для вибору перекладача
    Status for choosing a translator
    """
    if callback_query.data == "exit":
        await state.clear()
        await callback_query.message.edit_text(text="Ви вийшли!")
    else:
        await state.set_state(ts.lang)
        use_translator = callback_query.data.split(":")[1]

        await state.update_data(used_translator=use_translator)
        text = "Чудово!\nТепер виберіть мову."
        await callback_query.message.edit_text(reply_markup=choosing_language, text=text)


@router.callback_query(ts.lang)
async def language(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Статус для вибору мови
    Status for language selection
    """
    if callback_query.data == "exit":
        await state.clear()
        await callback_query.message.edit_text(text="Ви вийшли!")
    else:
        await state.set_state(ts.text)
        language = callback_query.data.split(":")[1]

        await state.update_data(language=language)
        await callback_query.message.edit_text(text="Пишіть повідомлення яке треба перекласти")
    

@router.message(ts.text)
async def text(message: types.Message, state: FSMContext):
    """
    Статус для кінцевого перекладу
    Status for final translation
    """
    if len(message.text) > 2000:
        await message.reply("Ваше повідомлення занадто довге. Будь ласка, надішліть повідомлення до 2000 символів.")
        return

    text = message.text
    data = await state.get_data()

    try:
        await message.answer(text="Це може зайняти деякий час...")
        translator_func = getattr(tss, data.get("used_translator"), None)
        if translator_func:
            translated_text = str(translator_func(text, to_language=str(data.get("language"))))
            await message.answer(text=translated_text)
        else:
            await message.answer(text="Вибраний вами перекладач не знайдений\nнапишіть !report"
                                      " або /report з рекомендацією щоб я добавив цей "
                                      "перекладач")
    except Exception as ex:
        logging.error(f"An unexpected error occurred in translator: {ex}")
        await message.answer(text="Вибачте, сталася помилка під час перекладу.")
    finally:
        await state.clear()
