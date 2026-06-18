import logging
from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot

from database import (
    count_all,
    count_this_week,
    count_today,
    count_users,
    get_all_user_ids,
    get_unreminded_registrations,
    mark_reminded,
)

UZT = timezone(timedelta(hours=5))

DAY_NAMES = [
    "Dushanba", "Seshanba", "Chorshanba",
    "Payshanba", "Juma", "Shanba", "Yakshanba",
]


async def send_daily_hours(bot: Bot, admin_id: int) -> None:
    """Har kuni 8:00 UZT da barcha foydalanuvchilarga ish vaqti xabari."""
    now = datetime.now(UZT)
    day = DAY_NAMES[now.weekday()]

    text = (
        f"🌅 <b>Xayrli tong!</b>\n\n"
        f"📅 Bugun {day}, {now.strftime('%d.%m.%Y')}\n\n"
        f"⏰ <b>Qabul vaqti:</b> 9:00 — 18:00\n\n"
        f"📝 Ro'yxatdan o'tish uchun:\n"
        f"👉 /start"
    )

    user_ids = await get_all_user_ids()
    ok = 0
    for uid in user_ids:
        try:
            await bot.send_message(uid, text)
            ok += 1
        except Exception:
            pass

    logging.info("Kunlik xabar: %d/%d foydalanuvchiga yuborildi", ok, len(user_ids))


async def send_weekly_report(bot: Bot, admin_id: int) -> None:
    """Har dushanba 9:00 UZT da adminga haftalik hisobot."""
    total = await count_all()
    this_week = await count_this_week()
    today = await count_today()
    users = await count_users()

    now = datetime.now(UZT)
    text = (
        f"📊 <b>Haftalik hisobot</b>\n"
        f"📅 {now.strftime('%d.%m.%Y, %H:%M')}\n\n"
        f"👥 <b>Jami botga kirishganlar:</b> {users} ta\n"
        f"📋 <b>Jami arizalar:</b> {total} ta\n"
        f"📆 <b>Shu hafta arizalar:</b> {this_week} ta\n"
        f"📌 <b>Bugun arizalar:</b> {today} ta"
    )

    try:
        await bot.send_message(admin_id, text)
        logging.info("Haftalik hisobot adminga yuborildi")
    except Exception:
        logging.exception("Haftalik hisobot yuborib bo'lmadi")


async def check_24h_reminders(bot: Bot, admin_id: int) -> None:
    """Har soatda: 24 soat o'tib javob berilmagan arizalar bo'yicha adminga eslatma."""
    regs = await get_unreminded_registrations()
    for reg_id, full_name, grade, phone, created_at in regs:
        text = (
            f"⏰ <b>Eslatma! 24 soat o'tdi</b>\n\n"
            f"Ariza <b>#{reg_id}</b> bo'yicha hali bog'lanilmagan:\n\n"
            f"👤 {full_name}\n"
            f"🏫 {grade}-sinf\n"
            f"📞 {phone}\n"
            f"🕐 Ariza vaqti: {created_at}\n\n"
            f"Iltimos, tezroq bog'laning! 🙏"
        )
        try:
            await bot.send_message(admin_id, text)
            await mark_reminded(reg_id)
        except Exception:
            logging.exception("Eslatma yuborib bo'lmadi: ariza #%d", reg_id)


def setup_scheduler(bot: Bot, admin_id: int) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()

    # Har kuni 8:00 UZT = 3:00 UTC
    scheduler.add_job(
        send_daily_hours,
        CronTrigger(hour=3, minute=0),
        args=[bot, admin_id],
        id="daily_hours",
        replace_existing=True,
    )

    # Har dushanba 9:00 UZT = 4:00 UTC
    scheduler.add_job(
        send_weekly_report,
        CronTrigger(day_of_week="mon", hour=4, minute=0),
        args=[bot, admin_id],
        id="weekly_report",
        replace_existing=True,
    )

    # Har soatda: 24h eslatma tekshiruvi
    scheduler.add_job(
        check_24h_reminders,
        "interval",
        hours=1,
        args=[bot, admin_id],
        id="reminder_check",
        replace_existing=True,
    )

    return scheduler
