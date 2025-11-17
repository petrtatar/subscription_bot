from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from ..services.payments import create_payment

router = Router()


@router.message(Command("buy"))
async def on_buy(message: Message):
    price = 100
    payment_url, payment_id = await create_payment(amount=price, tg_id=message.from_user.id)
    await message.answer(f"{payment_url} {payment_id}")
