"""
Файл для мідлварі ThrottlingMiddleware
The file for the ThrottlingMiddleware middleware
"""
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    """
    Middleware для обмеження частоти запитів від користувачів.
    """
    def __init__(self, rate_limit: float = 0.7) -> None:
        self.cache = TTLCache(maxsize=10_000, ttl=rate_limit)

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if event.chat.id in self.cache:
            return
        self.cache[event.chat.id] = None
        return await handler(event, data)
