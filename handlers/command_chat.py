import logging
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode
from openai import AsyncOpenAI, RateLimitError, APIError
import translators.server as tss

from keyboards.chat import keyboard
from states.chat import Chat
import config

router = Router()

async def answer_chat(text):
    client = AsyncOpenAI(api_key=config.OPENAI_TOKEN)
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": config.SYSTEM_MESSAGE},
                {"role": "user", "content": text},
            ],
            top_p=1,
            max_tokens=500
        )
        return response.choices[0].message.content.replace("`", "*")

    except RateLimitError:
        logging.warning("OpenAI API rate limit exceeded.")
        return "Вибачте, досягнуто ліміту запитів до OpenAI. Спробуйте пізніше."
    except APIError as ex:
        logging.error(f"OpenAI API error: {ex}")
        return "Вибачте, сталася помилка на стороні OpenAI. Спробуйте пізніше."
    except Exception as ex:
        logging.error(f"An unexpected error occurred in answer_chat: {ex}")
        return "Вибачте, сталася невідома помилка. Спробуйте повторити запит пізніше."
    

@router.callback_query(F.data == "delete")
async def delete(callback_query: types.CallbackQuery):
    await callback_query.message.delete()


@router.callback_query()
async def continue_chat(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(text=callback_query.message.text + "\n\nДобре задавайте своє питання.")
    await state.set_state(Chat.warning_and_start_chat)


@router.message(Chat.warning_and_start_chat)
async def chat(message: types.Message, state: FSMContext):
    if message.text.lower() == "вийти":
        await state.clear()
        await message.reply("Ви вийшли з режиму чату.")
        return

    if len(message.text) > 2000:
        await message.reply("Ваше повідомлення занадто довге. Будь ласка, надішліть повідомлення до 2000 символів.")
        return
    else:
        processing_message = await message.answer(text="Зачекайте будь ласка, це може зайнняти деякий час.")
        answer = await answer_chat(message.text)
        try:
            await processing_message.edit_text(text=answer, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
        except Exception:
            await processing_message.delete()
            await message.answer(text=answer, reply_markup=keyboard)
        finally:
            await state.clear()


@router.message(Command("chat"))
async def warning_and_start_chat(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in config.PREMIUM_USERS:
        await message.answer(text="ПОПЕРЕДЖЕННЯ!\n"
                                  "Офіційний API який використовує автор є чуть-чуть глюканутий.\n"
                                  "А саме GPT може відповідати не правильно, криво і так далі.\n"
                                  "То вам рекомендується формулювати свої питання по різному.\n"
                                  "Добре задавайте своє питання.")
        await state.set_state(Chat.warning_and_start_chat)
    else:
        await message.answer(text="Вибачте але ви не в списку преміум користувачів!\n"
                                  "Зверніться до автора щоб вас додали до цього списку.")
