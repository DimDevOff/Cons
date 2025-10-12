"""
Фалй для надсилання диних про погоду
"""
import requests
import json

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
import translators.server as tss

import config
from create_bot import bot
from states.weather import Weather

router = Router()

@router.message(Command("weather", prefix="/"))
async def weather(message: types.Message, state: FSMContext):
    """
    Головна функція яка включається, коли користувач пише </weather>
    """
    chat_id = message.chat.id
    user_id = message.from_user.id
    try:
        with open("json/weather.json", 'r') as weather_file:
            weather_json = json.load(weather_file)
        await bot.send_message(chat_id=chat_id, text=get_weather(weather_json[str(user_id)]))
    except (FileNotFoundError, KeyError):
        await bot.send_message(chat_id=chat_id, text="Напишіть назву міста за замовчуванням")
        await state.set_state(Weather.city)

@router.message(Command("weather", prefix="!"))
async def weather_change_city(message: types.Message, state: FSMContext):
    """
    Головна функція яка включається, коли користувач пише </weather !>
    """
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text="Напишіть назву міста за замовчуванням")
    await state.set_state(Weather.city)


def get_weather(city):
    r = requests.get(url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.WEATHER_TOKEN}"
                         f"&units=metric")

    weather_result = r.json()
    if weather_result["cod"] == 200:
        try:
            city_name = weather_result["name"]
            humidity = weather_result["main"]["humidity"]
            weather = tss.google(weather_result["weather"][0]["description"], to_language="uk")
            temp = weather_result["main"]["temp"]
            wind_speed = weather_result["wind"]["speed"]
            text = f"Місто: {city_name}\n" \
                f"Вологість: {humidity}%\n" \
                f"Погода: {weather}\n" \
                f"Температура: {temp}°C\n" \
                f"Швидкість вітру: {wind_speed}"

            return text
        except Exception as e:
            return f"Вибачте але сталася помилка!\nСпробуйте пізніше або зверніться до автора.\n{e}"
    elif weather_result["cod"] == "404":
        return "Вибачте!\nНе вдалося получити дані про місто."
    else:
        return "Вибачте!\nСталася не відома помилка."


@router.message(Weather.city)
async def choose_city(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text="Секунду...")
    if message.text == "Гусятин":
        city = "Husiatyn"
    else:
        city = tss.google(message.text, to_language='en')
    
    try:
        with open("json/weather.json", 'r') as weather_file:
            weather_json = json.load(weather_file)
    except (FileNotFoundError, json.JSONDecodeError):
        weather_json = {}

    weather_json[str(message.from_user.id)] = city

    with open("json/weather.json", 'w') as weather_file:
        json.dump(weather_json, weather_file, ensure_ascii=False, indent=4)

    await bot.send_message(chat_id=chat_id, text=get_weather(city))

    await state.clear()
