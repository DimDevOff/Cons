from aiogram import Router

from . import command_save_open
from . import command_start_help
from . import command_report
from . import command_translator
from . import command_weather
from . import command_games
from . import command_rate
from . import command_chat

def get_routers() -> list[Router]:
    return [
        command_start_help.router,
        command_report.router,
        command_translator.router,
        command_weather.router,
        command_games.router,
        command_rate.router,
        command_chat.router,
        command_save_open.router,
    ]
