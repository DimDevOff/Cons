"""
Файл для запуску бота
The file for starting the bot
"""
import asyncio
import logging

from create_bot import dp, bot
from handlers import command_report, command_start_help, command_translator, command_weather, command_games, command_rate, command_chat, command_save_open

logging.basicConfig(level=logging.INFO)

from middlewares.throttling import ThrottlingMiddleware

async def main():
    dp.message.middleware(ThrottlingMiddleware())
    dp.include_router(command_report.router)
    dp.include_router(command_start_help.router)
    dp.include_router(command_translator.router)
    dp.include_router(command_weather.router)
    dp.include_router(command_games.router)
    dp.include_router(command_rate.router)
    dp.include_router(command_chat.router)
    dp.include_router(command_save_open.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
