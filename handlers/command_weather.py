"""
Фалй для надсилання диних про погоду
"""
import logging
import requests
import json
import os

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
import translators.server as tss

import config
from states.weather import Weather
from utils import sanitize_html

router = Router()

@router.message(Command("weather", prefix="/"))
async def weather(message: types.Message, state: FSMContext):
    """
    Головна функція яка включається, коли користувач пише </weather>
    """
    user_id = message.from_user.id
    try:
        with open("json/weather.json", 'r') as weather_file:
            weather_json = json.load(weather_file)
        await message.answer(text=get_weather(weather_json[str(user_id)]))
    except (FileNotFoundError, KeyError):
        await message.answer(text="Напишіть назву міста за замовчуванням")
        await state.set_state(Weather.city)

@router.message(Command("weather", prefix="!"))
async def weather_change_city(message: types.Message, state: FSMContext):
    """
    Головна функція яка включається, коли користувач пише </weather !>
    """
    await message.answer(text="Напишіть назву міста за замовчуванням")
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
        except requests.exceptions.RequestException as e:
            logging.error(f"Request error in get_weather: {e}")
            return "Вибачте, сталася помилка при отриманні даних про погоду."
        except Exception as e:
            logging.error(f"An unexpected error occurred in get_weather: {e}")
            return "Вибачте, сталася невідома помилка."
    elif weather_result["cod"] == "404":
        return "Вибачте!\nНе вдалося получити дані про місто."
    else:
        return "Вибачте!\nСталася не відома помилка."


@router.message(Weather.city)
async def choose_city(message: types.Message, state: FSMContext):
    city_name = sanitize_html(message.text)
    if len(city_name) > 100:
        await message.reply("Назва міста занадто довга. Будь ласка, введіть назву до 100 символів.")
        return

    loading_msg = await message.answer(text="Секунду...")

    if city_name == "Гусятин":
        city_for_api = "Husiatyn"
    else:
        city_for_api = tss.google(city_name, to_language='en')

    # Ensure the json directory exists
    json_dir = "json"
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)
    
    weather_file_path = os.path.join(json_dir, "weather.json")

    try:
        with open(weather_file_path, 'r', encoding='utf-8') as weather_file:
            weather_json = json.load(weather_file)
    except (FileNotFoundError, json.JSONDecodeError):
        weather_json = {}

    weather_json[str(message.from_user.id)] = city_for_api

    with open(weather_file_path, 'w', encoding='utf-8') as weather_file:
        json.dump(weather_json, weather_file, ensure_ascii=False, indent=4)

    await loading_msg.delete()
    await message.answer(text=get_weather(city_for_api))
    await state.clear()
