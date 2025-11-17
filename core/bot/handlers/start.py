from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           ReplyKeyboardRemove)
from ..utils.db import upsert_profile, save_phone_by_tg_id, get_user_by_tg_id
from ..keyboards.main_menu import main_menu_inline
from ...botdata.models import Subscription
from ..utils.db import get_or_create_subscription

router = Router()


@router.message(Command("start"))
async def on_start(message: types.Message) -> None:
    get_user = await get_user_by_tg_id(message.from_user.id)
    if not get_user:
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
    else:
        await message.answer(
            f"Меню.",
            reply_markup=main_menu_inline
        )


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
