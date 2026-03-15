"""
Файл для запуску бота
The file for starting the bot
"""
import asyncio
import logging

from create_bot import dp, bot
from handlers import get_routers

logging.basicConfig(level=logging.INFO)

from middlewares.throttling import ThrottlingMiddleware

async def main():
    dp.message.middleware(ThrottlingMiddleware())

    for router in get_routers():
        dp.include_router(router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
