import requests
import json

from aiogram import Router, types
from aiogram.filters import Command

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


@router.message(Command("rate"))
async def rate(message: types.Message):
    loading_msg = await message.answer(text="Секунду...")
    await loading_msg.delete()
    await message.answer(text="Ця інформація взята з офіційного API ПриватБанку\n" + get_rate())
