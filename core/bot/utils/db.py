from asgiref.sync import sync_to_async
from core.botdata.models import UserProfile, Subscription


@sync_to_async
def upsert_profile(tg_id: int, username: str | None, full_name: str | None) -> UserProfile:
    obj, _created = UserProfile.objects.update_or_create(
        telegram_id=tg_id,
        defaults={
            "username": username,
            "full_name": full_name,
        },
    )
    return obj


@sync_to_async
def save_phone_by_tg_id(tg_id: int, phone: str) -> int:
    return UserProfile.objects.filter(telegram_id=tg_id).update(phone=phone)


@sync_to_async
def get_user_by_tg_id(tg_id: int) -> UserProfile | None:
    return UserProfile.objects.filter(telegram_id=tg_id).first()


@sync_to_async
def get_or_create_subscription(user):
    return Subscription.objects.get_ot_create(user=user)
