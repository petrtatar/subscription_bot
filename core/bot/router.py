from aiogram import Router
from .handlers import start, profile, create_payment


def setup_router(dp):
    router = Router()
    router.include_router(start.router)
    router.include_router(profile.router)
    router.include_router(create_payment.router)
    dp.include_router(router)
