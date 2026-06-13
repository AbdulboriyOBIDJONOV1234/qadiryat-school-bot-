from datetime import date

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import BufferedInputFile, Message

from config import ADMIN_ID
from database import count_all, count_today, get_all_registrations
from excel_export import build_excel
from keyboards import get_admin_keyboard

admin_router = Router()
admin_router.message.filter(F.from_user.id == ADMIN_ID)

ADMIN_WELCOME = (
    "👋 <b>Salom, Admin!</b>\n\n"
    "Bu — <b>Qadriyat maktabi</b> ro'yxatga olish botining boshqaruv paneli.\n\n"
    "📊 <b>Statistika</b> — ro'yxatdan o'tganlar sonini ko'rsatadi\n"
    "📥 <b>Excel hisobot</b> — barcha arizalarni Excel faylda yuboradi"
)


@admin_router.message(CommandStart())
async def admin_start(message: Message):
    await message.answer(ADMIN_WELCOME, reply_markup=get_admin_keyboard())


@admin_router.message(F.text.in_({"📊 Statistika", "/stats"}))
async def admin_stats(message: Message):
    total = count_all()
    today = count_today()
    await message.answer(
        f"📋 <b>Jami arizalar:</b> {total} ta\n"
        f"📅 <b>Bugun:</b> {today} ta"
    )


@admin_router.message(F.text.in_({"📥 Excel hisobot", "/export"}))
async def admin_export(message: Message):
    rows = get_all_registrations()
    if not rows:
        await message.answer("Hozircha hech kim ro'yxatdan o'tmagan.")
        return

    excel_bytes = build_excel(rows)
    today_str = date.today().strftime("%d.%m.%Y")
    filename = f"Qadriyat_royxat_{today_str}.xlsx"

    await message.answer_document(
        BufferedInputFile(excel_bytes, filename=filename),
        caption=f"📊 Jami {len(rows)} ta ariza ({today_str})",
    )
