from aiogram import Router, types, F
from datetime import datetime, timezone
from ..utils.db import get_user_by_tg_id

router = Router()


@router.callback_query(F.data == "show_profile")
async def show_profile(callback: types.CallbackQuery):
    now = datetime.now(timezone.utc)
    user = await get_user_by_tg_id(callback.from_user.id)
    if not user:
        await callback.message.answer("Пользователь не найден.")
        return

    if user.subscription_expires_at and user.subscription_expires_at > now:
        sub_status = f"Активна до {user.subscription_expires_at.strftime('%d.%m.%Y')}"
    else:
        sub_status = "Отсутствует"

    text = (
        f"👤Имя: {user.full_name or '-'}\n"
        f"📞Телефон: {user.phone or '-'}\n"
        f"💳Подписка: {sub_status}\n"
        f"💰Бонусный баланс: {user.bonus_balance}"
    )
    await callback.message.answer(text)
    await callback.answer()
