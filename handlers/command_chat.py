from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode
from openai import AsyncOpenAI
import translators.server as tss

from keyboards.chat import keyboard
from create_bot import bot
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
        return response.choices[0].message.content.replace("```", "**")
    
    except Exception as ex:
        if "That model is currently overloaded with other requests." in str(ex):
            return "Вибачте але зараз сервери перегруженні і вони не відповідають на запити."
        else:
            return f"Вибачте але зараз виникла невідома помилка.\n" \
                   f"Спробуйте повторити питання пізніше.\nОпис помилки: {ex}"
    

@router.callback_query(F.data == "delete")
async def delete(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)


@router.callback_query()
async def continue_chat(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text=callback_query.message.text + "\n\nДобре задавайте своє питання.")
    await state.set_state(Chat.warning_and_start_chat)


@router.message(Chat.warning_and_start_chat)
async def chat(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    if message.text.lower() == "вийти":
        await state.clear()
    else:
        await bot.send_message(chat_id=chat_id, text="Зачекайте будь ласка, це може зайнняти деякий час.")
        answer = await answer_chat(message.text)
        try:
            await bot.edit_message_text(chat_id=chat_id, message_id=message.message_id + 1, text=answer,
                                        reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
            await state.clear()
        except:
            await bot.send_message(chat_id=chat_id, text=answer, reply_markup=keyboard)
            await state.clear()


@router.message(commands=["chat"])
async def warning_and_start_chat(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if user_id in config.PREMIUM_USERS:
        await bot.send_message(chat_id=chat_id,
                               text="ПОПЕРЕДЖЕННЯ!\n"
                                    "Офіційний API який використовує автор є чуть-чуть глюканутий.\n"
                                    "А саме GPT може відповідати не правильно, криво і так далі.\n"
                                    "То вам рекомендується формулювати свої питання по різному.\n"
                                    "Добре задавайте своє питання.")
        await state.set_state(Chat.warning_and_start_chat)
    else:
        await bot.send_message(chat_id=chat_id,
                               text="Вибачте але ви не в списку преміум користувачів!\n"
                                    "Зверніться до автора щоб вас додали до цього списку.")
