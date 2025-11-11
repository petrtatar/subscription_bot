import asyncio
import os
from datetime import datetime, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from asgiref.sync import sync_to_async
from botdata.models import Broadcast, UserProfile
from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))


@sync_to_async
def get_unsent_broadcasts():
    now = datetime.now(timezone.utc)
    return list(Broadcast.objects.filter(sent=False, send_at__lte=now) | Broadcast.objects.filter(sent=False, send_at=None))


@sync_to_async
def mark_sent(broadcast):
    broadcast.sent = True
    broadcast.save()


@sync_to_async
def get_all_users():
    return list(UserProfile.objects.all())


async def send_broadcast(broadcast):
    users = await get_all_users()
    for u in users:
        try:
            if broadcast.media:
                await bot.send_document(u.telegram_id, open(broadcast.media.path, "rb"), caption=broadcast.text or "")
            else:
                await bot.send_message(u.telegram_id, broadcast.text or "")
        except Exception:
            continue
    await mark_sent(broadcast)


async def check_broadcasts():
    broadcasts = await get_unsent_broadcasts()
    if broadcasts:
        print(f"Найдено {len(broadcasts)} рассылок для отправки")
        for b in broadcasts:
            await send_broadcast(b)
    else:
        print("Нет новых рассылок")


def start_scheduler():
    print("Запуск планировщика")
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_broadcasts, "interval", seconds=30)
    print("Планировщик запущен")
    scheduler.start()
