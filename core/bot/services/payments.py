import yookassa
from yookassa import Payment
import uuid
from dotenv import load_dotenv
import os

load_dotenv()

yookassa.Configuration.account_id = os.getenv("YOOKASSA_SHOP_ID")
yookassa.Configuration.secret_key = os.getenv("YOOKASSA_SECRET_KEY")


async def create_payment(amount: int, tg_id: int):
    idempotence_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
            "value": amount,
            "currency": "RUB"
        },
        "payment_method_data": {
            "type": "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/Beburishvili_bot"
        },
        "capture": True,
        "metadata": {
            "tg_id": tg_id
        },
        "description": "Подписка"
    }, idempotence_key)

    # get confirmation url
    confirmation_url = payment.confirmation.confirmation_url

    return confirmation_url, payment.id
