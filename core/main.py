from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import Command
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardRemove)

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio

import os
import sys
import django
from asgiref.sync import sync_to_async

sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from botdata.models import UserProfile, Tariff
from scheduler import start_scheduler

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()
router = Router()
dp.include_router(router)


@sync_to_async
def upsert_profile(tg_id: int, username: str | None, full_name: str | None) -> UserProfile:
    obj, _created = UserProfile.objects.update_or_create(
        telegram_id = tg_id,
        defaults={
            "username": username,
            "full_name": full_name,
        },
    )
    return obj


@router.message(Command("start"))
async def on_start(message: types.Message) -> None:
    u = message.from_user
    full = (u.full_name or " ".join([x for x in [u.first_name, u.last_name] if x]) or None)
    await upsert_profile(tg_id=u.id, username=u.username, full_name=full)
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Поделиться телефоном", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Нажмите кнопку, чтобы поделиться номером"
    )
    await message.answer(f"Данныe профиля сохранены. Нажмите кнопку, чтобы добавить телефон",
                         reply_markup=kb)


@sync_to_async
def save_phone_by_tg_id(tg_id: int, phone: str) -> int:
    return UserProfile.objects.filter(telegram_id=tg_id).update(phone=phone)


@router.message(F.contact)
async def on_contact(message: types.Message) -> None:
    c = message.contact
    phone = c.phone_number
    owner_id = c.user_id or message.from_user.id
    updated = await save_phone_by_tg_id(owner_id, phone)
    await message.answer(
        "Телефон сохранен." if updated else "Профиль не найден. Нажмите /start и повторите.",
        reply_markup=ReplyKeyboardRemove(),
    )


async def main():
    start_scheduler()

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
