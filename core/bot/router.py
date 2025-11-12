from aiogram import Router
from .handlers import start, profile


def setup_router(dp):
    router = Router()
    router.include_router(start.router)
    router.include_router(profile.router)
    dp.include_router(router)
