from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Мой профиль", callback_data="show_profile")],
        [InlineKeyboardButton(text="Купить подписку", callback_data="buy_subscription")]
    ]
)
