import asyncio
from datetime import date

from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery, Message

from config import ADMIN_ID
from database import (
    count_all,
    count_today,
    delete_all_registrations,
    get_all_registrations,
    get_all_user_ids,
    get_registration_by_id,
    update_registration_status,
)
from excel_export import build_excel
from keyboards import get_admin_keyboard, get_reset_confirm_keyboard
from states import Broadcast

admin_router = Router()
admin_router.message.filter(F.from_user.id == ADMIN_ID)
admin_router.callback_query.filter(F.from_user.id == ADMIN_ID)

ADMIN_WELCOME = (
    "👋 <b>Salom, Admin!</b>\n\n"
    "Bu — <b>Qadriyat maktabi</b> ro'yxatga olish botining boshqaruv paneli.\n\n"
    "📊 <b>Statistika</b> — ro'yxatdan o'tganlar sonini ko'rsatadi\n"
    "📥 <b>Excel hisobot</b> — barcha arizalarni Excel faylda yuboradi\n"
    "📢 <b>Xabar yuborish</b> — barcha foydalanuvchilarga xabar jo'natadi\n"
    "🗑️ <b>Bazani tozalash</b> — test arizalarini o'chirish uchun"
)


@admin_router.message(CommandStart())
async def admin_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(ADMIN_WELCOME, reply_markup=get_admin_keyboard())


@admin_router.message(F.text.in_({"📊 Statistika", "/stats"}))
async def admin_stats(message: Message):
    total = await count_all()
    today = await count_today()
    await message.answer(
        f"📋 <b>Jami arizalar:</b> {total} ta\n"
        f"📅 <b>Bugun:</b> {today} ta"
    )


@admin_router.message(F.text.in_({"📥 Excel hisobot", "/export"}))
async def admin_export(message: Message):
    rows = await get_all_registrations()
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


# ───── RESET ─────

@admin_router.message(F.text.in_({"🗑️ Bazani tozalash", "/reset"}))
async def admin_reset_ask(message: Message):
    total = await count_all()
    await message.answer(
        f"⚠️ <b>Diqqat!</b>\n\n"
        f"Hozir bazada <b>{total} ta ariza</b> bor.\n"
        f"Barchasini o'chirmoqchimisiz?\n\n"
        f"Bu amalni orqaga qaytarib bo'lmaydi!",
        reply_markup=get_reset_confirm_keyboard(),
    )


@admin_router.callback_query(F.data == "reset_confirm")
async def admin_reset_confirm(callback: CallbackQuery):
    deleted = await delete_all_registrations()
    await callback.message.edit_text(
        f"✅ <b>Baza tozalandi!</b>\n"
        f"🗑️ {deleted} ta ariza o'chirildi. ID hisoblagich 1 dan qayta boshlandi."
    )
    await callback.answer()


@admin_router.callback_query(F.data == "reset_cancel")
async def admin_reset_cancel(callback: CallbackQuery):
    await callback.message.edit_text("❌ Tozalash bekor qilindi. Hech narsa o'chirilmadi.")
    await callback.answer()


# ───── BROADCAST ─────

@admin_router.message(F.text.in_({"📢 Xabar yuborish", "/broadcast"}))
async def admin_broadcast_ask(message: Message, state: FSMContext):
    await state.set_state(Broadcast.waiting_for_message)
    await message.answer(
        "✍️ <b>Yubormoqchi bo'lgan xabaringizni yozing:</b>\n\n"
        "Matn, rasm, video — istalgan formatda.\n"
        "Bekor qilish uchun /bekor yuboring.",
    )


@admin_router.message(Command("bekor"), Broadcast.waiting_for_message)
async def admin_broadcast_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Xabar yuborish bekor qilindi.", reply_markup=get_admin_keyboard())


@admin_router.message(Broadcast.waiting_for_message)
async def admin_broadcast_send(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    user_ids = await get_all_user_ids()

    if not user_ids:
        await message.answer(
            "❗ Hozircha botdan foydalangan foydalanuvchilar yo'q.",
            reply_markup=get_admin_keyboard(),
        )
        return

    status_msg = await message.answer(f"📤 Yuborilmoqda... (0/{len(user_ids)})")

    sent = 0
    failed = 0
    for i, uid in enumerate(user_ids, 1):
        try:
            await message.copy_to(uid)
            sent += 1
        except Exception:
            failed += 1
        if i % 10 == 0:
            try:
                await status_msg.edit_text(f"📤 Yuborilmoqda... ({i}/{len(user_ids)})")
            except Exception:
                pass
        await asyncio.sleep(0.05)

    await status_msg.edit_text(
        f"✅ <b>Xabar yuborildi!</b>\n\n"
        f"👥 Jami: {len(user_ids)} ta\n"
        f"✅ Muvaffaqiyatli: {sent} ta\n"
        f"❌ Bloklaganlar / xato: {failed} ta"
    )
    await message.answer("Boshqa buyruq:", reply_markup=get_admin_keyboard())


# ───── ARIZA HOLATI ─────

_STATUS_MAP = {
    "accepted": ("accepted", "✅ Qabul qilindi",
                 "🎉 <b>Tabriklaymiz!</b>\n\nSizning arizangiz <b>qabul qilindi!</b>\n"
                 "Tez orada operatorlarimiz siz bilan bog'lanadi.\n\n"
                 "Savollar uchun: @qadriyat_schooladmin"),
    "review":   ("review",   "🔄 Ko'rilmoqda",
                 "🔄 Sizning arizangiz <b>ko'rib chiqilmoqda.</b>\n"
                 "Tez orada javob beramiz.\n\n"
                 "Savollar uchun: @qadriyat_schooladmin"),
    "rejected": ("rejected", "❌ Rad etildi",
                 "😔 Afsuski, sizning arizangiz <b>rad etildi.</b>\n"
                 "Batafsil ma'lumot uchun adminimizga murojaat qiling:\n\n"
                 "👤 @qadriyat_schooladmin\n"
                 "📞 +998 90 105-77-78"),
}


@admin_router.callback_query(F.data.startswith("st_"))
async def status_callback(callback: CallbackQuery, bot: Bot):
    parts = callback.data.split("_", 2)
    if len(parts) != 3:
        await callback.answer("Xatolik!")
        return

    _, key, reg_id_str = parts
    if key not in _STATUS_MAP or not reg_id_str.isdigit():
        await callback.answer("Noto'g'ri ma'lumot!")
        return

    reg_id = int(reg_id_str)
    status_code, label, user_msg = _STATUS_MAP[key]

    await update_registration_status(reg_id, status_code)

    reg = await get_registration_by_id(reg_id)
    if reg:
        _, telegram_id, full_name, grade, phone = reg
        if telegram_id and telegram_id != 0:
            try:
                await bot.send_message(
                    telegram_id,
                    f"📋 <b>Ariza #{reg_id} holati yangilandi</b>\n\n{user_msg}",
                )
            except Exception:
                pass

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer(f"✅ {label}")
