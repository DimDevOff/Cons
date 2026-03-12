"""
Файл для ігор
"""
from random import randint

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from states.games import Games

router = Router()

@router.message(Command("games"))
async def games(message: types.Message, state: FSMContext):
    """
    Якщо користувач пише /games то бот відправляє повідомлення й переходе в стан сhoose_game
    """
    text =  "Виберіть гру (по номеру) щоб вийти напишіть \"Вийти\"\n" \
            "1 - Камінь ножниці папір\n" \
            "2 - Вгадай число"
    await message.answer(text=text)
    await state.set_state(Games.choose_game)
    
    
@router.message(Games.choose_game)
async def choose_game(message: types.Message, state: FSMContext):
    """
    Користувач пише число і його перекидує до відповідної гри
    """
    choose_game = message.text.lower()
    match choose_game:
        case "1":
            await message.answer(text="Виберіть число:\n1 - камінь\n2 - ножниці\n3 - папір")
            await state.set_state(Games.rock_paper_scissors)
        case "2":
            await message.answer(text="Число від -10 до 10 загадане! Щоб вийти наришіть \"Вийти\"")
            await state.set_state(Games.guess_number)
        case "вийти":
            await message.answer(text="Ви вийшли з меню!")
            await state.clear()
        case _:
            await message.answer(text="Виберіть гру числом наприклад: 2")


@router.message(Games.guess_number)
async def game_guess_number(message: types.Message, state: FSMContext):
    message_text = message.text
    random_number = randint(-10, 10)
    try:
        user_number = int(message_text)
        if user_number == random_number:
            await message.answer(text="Ви вгадали загадане число!")
        else:
            await message.answer(text="Не вгадав!")
    except ValueError:
        if message_text.lower() == "вийти":
            await message.answer(text="Ви вийшли!")
            await state.clear()
        else:
            await message.answer(text="Напишіть число")


@router.message(Games.rock_paper_scissors)
async def game_rock_paper_scissors(message: types.Message, state: FSMContext):
    message_text = message.text.lower()
    random_object = randint(1, 3)
    match message_text:
        case "вийти":
            await message.answer(text="Ви вийшли з гри!")
            await state.clear()
        case _:
            try:
                user_choice = int(message_text)
                await message.answer(text=game_rock_paper_scissors_work(user_choice, random_object))
            except ValueError:
                await message.answer(text="Пишіть число або щоб вийти напишіть \"Вийти\"\n"
                                          "Виберіть число:\n1 - камінь\n2 - ножниці\n3 - папір")


def game_rock_paper_scissors_work(user_choice, random_object):
    if user_choice == random_object:
        return "Нічія!"
    else:
        match user_choice:
            case 1:
                match random_object:
                    case 2:
                        return "🤜✌️\nВи виграли!"
                    case _:
                        return "🤜🫲\nВи програли!"
            case 2:
                match random_object:
                    case 1:
                        return "✌️🤛\nВи програли!"
                    case _:
                        return "✌️🫲\nВи виграли!"
            case 3:
                match random_object:
                    case 1:
                        return "🫱🤛\nВи виграли!"
                    case _:
                        return "🫱✌️\nВи програли!"
            case _:
                return "Предмет не знайдений\nВиберіть число:\n1 - камінь\n2 - ножниці\n3 - папір"
