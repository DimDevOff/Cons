import requests
import json

from aiogram import Router, types

from create_bot import bot

router = Router()

def get_rate():
    r = requests.get(url=f"https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5")
    r = r.content.decode('utf-8')
    rjson = json.loads(r)
    EUR = float(rjson[0]["buy"])
    USD = float(rjson[1]["buy"])
    rate = f"Євро: {EUR:.2f}грн\n" \
           f"Долар: {USD:.2f}грн"
    return rate


@router.message(commands=["rate"])
async def rate(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text="Секунду...")
    await bot.delete_message(chat_id=chat_id, message_id=message.message_id+1)
    await bot.send_message(chat_id=chat_id, text="Ця інформація взята з офіційного API ПриватБанку\n" + get_rate())
