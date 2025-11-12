from aiogram import Bot, Dispatcher
import asyncio

import os
import sys
import django

sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from bot.router import setup_router
from scheduler import start_scheduler

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()
setup_router(dp)


async def main():
    start_scheduler()

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
