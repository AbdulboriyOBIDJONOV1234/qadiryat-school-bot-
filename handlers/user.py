import logging

from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from config import ADMIN_ID
from database import add_registration, format_dt, get_user_registrations, save_user
from keyboards import get_phone_keyboard, get_share_keyboard, get_user_keyboard
from states import Registration
from validators import (
    is_valid_location,
    is_valid_name_part,
    normalize_phone,
    parse_birth_date,
    parse_grade,
)

user_router = Router()

WELCOME_TEXT = (
    "🎓✨ <b>Assalomu alaykum!</b>\n\n"
    "<b>QADRIYAT — Xususiy maktabi</b>\n"
    "Jahon tillari va matematikaga ixtisoslashtirilgan 🌍📐\n\n"
    "🇬🇧 English — xalqaro tajriba\n"
    "📚 Zamonaviy ta'lim\n"
    "🏆 Xalqaro sertifikatlar\n"
    "💡 Innovatsion yondashuv\n"
    "🧑‍🏫 Chet ellik mutaxassislar bilan birga\n"
    "🎓 1-sinfdan 11-sinfgacha\n"
    "🇺🇿🇷🇺 O'zbek va rus sinflari\n\n"
    "📍 <b>Manzil:</b> Farg'ona viloyati, Qo'shtepa tumani\n"
    "Sarmazor MFY, Sharq ko'chasi 28-uy\n"
    "(Mo'ljal: \"Global Texstil\" yonida)\n"
    "📞 <b>Telefon:</b> +998 90 105-77-78, +998 93 400-44-88\n\n"
    "Savol yoki muammo bo'lsa — adminimizga murojaat qiling: @qadriyat_schooladmin\n\n"
    "👇 Quyidagi tugmalardan birini tanlang:"
)

ASK_FIRST_NAME = "✏️ Ismingizni kiriting:"
ASK_LAST_NAME = "👤 Familiyangizni kiriting:"
ASK_PATRONYMIC = "👨‍👦 Otangizning ismini (sharifingizni) kiriting:"
ASK_BIRTH_DATE = "🎂 Tug'ilgan sanangizni kiriting (kun.oy.yil, masalan: 15.03.2012):"
ASK_GRADE = "🏫 Nechanchi sinfga o'qishga kirmoqchisiz? (1 dan 11 gacha raqam kiriting):"
ASK_LOCATION = "📍 Qaysi hudud / tuman / shahardan ekanligingizni yozing:"
ASK_PHONE = (
    "📞 Va nihoyat, aloqa uchun telefon raqamingizni yuboring "
    "(pastdagi tugma orqali yoki qo'lda kiriting, masalan: +998901234567):"
)

SUCCESS_TEXT = (
    "✅ <b>Arizangiz qabul qilindi!</b>\n\n"
    "Tez orada operatorlarimiz siz bilan bog'lanishadi. "
    "<b>Qadriyat maktabi</b>ni tanlaganingiz uchun tashakkur! 🎓🙏\n\n"
    "📢 Yangiliklar va e'lonlardan habardor bo'lib turing:\n"
    "👉 <a href=\"https://t.me/qadriyat_xususiy_maktab\">Kanalimizga a'zo bo'ling</a>"
)

HELP_TEXT = (
    "❓ <b>Yordam kerakmi?</b>\n\n"
    "Savol, muammo yoki taklif bo'lsa — adminimizga murojaat qiling:\n\n"
    "👤 <b>Admin:</b> @qadriyat_schooladmin\n\n"
    "📞 Telefon: +998 90 105-77-78\n"
    "📞 Telefon: +998 93 400-44-88\n\n"
    "💡 Ko'p so'raladigan savollarga javob: /faq\n\n"
    "Biz doim yordam berishga tayyormiz! 🙏"
)

FAQ_TEXT = (
    "❓ <b>Ko'p so'raladigan savollar</b>\n\n"
    "1️⃣ <b>Ro'yxatdan qanday o'tish mumkin?</b>\n"
    "   → «📝 Ro'yxatdan o'tish» tugmasini bosing. Operator 1–2 ish kuni ichida bog'lanadi.\n\n"
    "2️⃣ <b>Oylik to'lov qancha?</b>\n"
    "   → To'lov sinf va dasturga qarab belgilanadi.\n"
    "   Aniq narx uchun: @qadriyat_schooladmin\n\n"
    "3️⃣ <b>Chegirmalar bormi?</b>\n"
    "   → Ha! Batafsil: /narx\n\n"
    "4️⃣ <b>Dars vaqti qanday?</b>\n"
    "   → Darslar 8:00 da boshlanib, 17:00 da tugaydi. 3 mahal issiq ovqat beriladi.\n\n"
    "5️⃣ <b>Transport xizmati bormi?</b>\n"
    "   → Ha, barcha o'quvchilar uchun bepul transport mavjud.\n\n"
    "6️⃣ <b>Qaysi sinflarga qabul bor?</b>\n"
    "   → 1-sinfdan 11-sinfgacha. O'zbek va rus tili bo'limlari mavjud.\n\n"
    "📞 Boshqa savollar uchun: @qadriyat_schooladmin"
)

MANZIL_TEXT = (
    "📍 <b>Maktab manzili</b>\n\n"
    "Farg'ona viloyati, Qo'shtepa tumani\n"
    "Sarmazor MFY, Sharq ko'chasi 28-uy\n"
    "<i>(Mo'ljal: «Global Texstil» yonida)</i>\n\n"
    "📞 +998 90 105-77-78\n"
    "📞 +998 93 400-44-88\n\n"
    "🕐 <b>Ish vaqti:</b> 9:00 — 18:00"
)

NARX_TEXT = (
    "💰 <b>To'lov va chegirmalar</b>\n\n"
    "To'lov miqdori farzandingizning sinfi va\n"
    "tanlangan dasturga qarab belgilanadi.\n\n"
    "Aniq narx va shartlar uchun murojaat qiling:\n"
    "📞 +998 90 105-77-78\n"
    "📞 +998 93 400-44-88\n"
    "👤 @qadriyat_schooladmin\n\n"
    "✨ <b>Maxsus chegirmalar:</b>\n\n"
    "🏅 Prezident yoki Ibn Sino maktablari\n"
    "   imtihonlarida yuqori ball to'plagan o'quvchilar\n\n"
    "👨‍👩‍👧‍👦 Bir oiladan ikki va undan ortiq farzandlari\n"
    "   bizda ta'lim olayotgan oilalar\n\n"
    "🤝 Kam ta'minlangan oila farzandlari"
)



# ───── /start ─────

@user_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await save_user(message.from_user.id, message.from_user.username)
    await message.answer(WELCOME_TEXT, reply_markup=get_user_keyboard())


# ───── Ro'yxatdan o'tish tugmasi ─────

@user_router.message(F.text == "📝 Ro'yxatdan o'tish")
async def btn_register(message: Message, state: FSMContext):
    current = await state.get_state()
    if current is not None:
        await message.answer(
            "⚠️ Siz hozir ro'yxatdan o'tish jarayonidasiz.\n"
            "To'xtatish uchun ❌ tugmasini bosing."
        )
        return
    await state.set_state(Registration.first_name)
    await message.answer(ASK_FIRST_NAME, reply_markup=ReplyKeyboardRemove())


# ───── Mening arizalarim ─────

@user_router.message(F.text == "📋 Mening arizalarim")
async def btn_my_registrations(message: Message):
    rows = await get_user_registrations(message.from_user.id)
    if not rows:
        await message.answer(
            "📭 Siz hali ro'yxatdan o'tmagansiz.\n"
            "Ro'yxatdan o'tish uchun 📝 tugmasini bosing.",
            reply_markup=get_user_keyboard(),
        )
        return

    text = f"📋 <b>Sizning arizalaringiz ({len(rows)} ta):</b>\n"
    for r in rows:
        _, full_name, birth_date, grade, location, phone, created_at, *_ = r
        text += (
            f"\n──────────────\n"
            f"👤 {full_name}\n"
            f"🎂 {birth_date}\n"
            f"🏫 {grade}-sinf | 📍 {location}\n"
            f"📞 {phone}\n"
            f"🕐 {format_dt(created_at)}"
        )

    await message.answer(text, reply_markup=get_user_keyboard())


# ───── Yordam ─────

@user_router.message(F.text == "❓ Yordam")
@user_router.message(Command("help"))
async def btn_help(message: Message):
    await message.answer(HELP_TEXT, reply_markup=get_user_keyboard())


# ───── FAQ ─────

@user_router.message(Command("faq"))
async def btn_faq(message: Message):
    await message.answer(FAQ_TEXT, reply_markup=get_user_keyboard())


# ───── Manzil ─────

@user_router.message(F.text == "📍 Manzil")
@user_router.message(Command("manzil"))
async def btn_manzil(message: Message):
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="🗺 Xaritada ko'rish",
            url="https://maps.app.goo.gl/ihZaUE6aaKNv6W9R7",
        )
    ]])
    await message.answer(MANZIL_TEXT, reply_markup=kb)


# ───── Narx ─────

@user_router.message(F.text == "💰 Narx va chegirmalar")
@user_router.message(Command("narx"))
async def btn_narx(message: Message):
    await message.answer(NARX_TEXT, reply_markup=get_user_keyboard())


# ───── Bekor qilish ─────

@user_router.message(F.text == "❌ Ro'yxatdan o'tishni bekor qilish")
@user_router.message(Command("bekor"))
async def cmd_cancel(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer(
            "ℹ️ Hozirda faol jarayon yo'q.",
            reply_markup=get_user_keyboard(),
        )
        return
    await state.clear()
    await message.answer(
        "❌ Ro'yxatdan o'tish bekor qilindi.\n"
        "Qaytadan boshlash uchun 📝 tugmasini bosing.",
        reply_markup=get_user_keyboard(),
    )


# ───── Registration FSM ─────

@user_router.message(Registration.first_name, F.text)
async def process_first_name(message: Message, state: FSMContext):
    first_name = message.text.strip()
    if not is_valid_name_part(first_name):
        await message.answer("⚠️ Iltimos, ismingizni faqat harflar bilan, bitta so'z qilib kiriting.")
        return
    await state.update_data(first_name=first_name)
    await state.set_state(Registration.last_name)
    await message.answer(ASK_LAST_NAME)


@user_router.message(Registration.first_name)
async def process_first_name_invalid(message: Message):
    await message.answer("⚠️ Iltimos, ismingizni matn ko'rinishida yozing.")


@user_router.message(Registration.last_name, F.text)
async def process_last_name(message: Message, state: FSMContext):
    last_name = message.text.strip()
    if not is_valid_name_part(last_name):
        await message.answer("⚠️ Iltimos, familiyangizni faqat harflar bilan, bitta so'z qilib kiriting.")
        return
    await state.update_data(last_name=last_name)
    await state.set_state(Registration.patronymic)
    await message.answer(ASK_PATRONYMIC)


@user_router.message(Registration.last_name)
async def process_last_name_invalid(message: Message):
    await message.answer("⚠️ Iltimos, familiyangizni matn ko'rinishida yozing.")


@user_router.message(Registration.patronymic, F.text)
async def process_patronymic(message: Message, state: FSMContext):
    patronymic = message.text.strip()
    if not is_valid_name_part(patronymic):
        await message.answer("⚠️ Iltimos, otangizning ismini faqat harflar bilan, bitta so'z qilib kiriting.")
        return
    await state.update_data(patronymic=patronymic)
    await state.set_state(Registration.birth_date)
    await message.answer(ASK_BIRTH_DATE)


@user_router.message(Registration.patronymic)
async def process_patronymic_invalid(message: Message):
    await message.answer("⚠️ Iltimos, otangizning ismini matn ko'rinishida yozing.")


@user_router.message(Registration.birth_date, F.text)
async def process_birth_date(message: Message, state: FSMContext):
    birth_date = parse_birth_date(message.text)
    if birth_date is None:
        await message.answer(
            "⚠️ Sana noto'g'ri formatda yoki yaroqsiz. Iltimos, kun.oy.yil ko'rinishida "
            "kiriting (masalan: 15.03.2012)."
        )
        return
    await state.update_data(birth_date=birth_date.strftime("%d.%m.%Y"))
    await state.set_state(Registration.grade)
    await message.answer(ASK_GRADE)


@user_router.message(Registration.birth_date)
async def process_birth_date_invalid(message: Message):
    await message.answer("⚠️ Iltimos, tug'ilgan sanangizni matn ko'rinishida yozing (kun.oy.yil).")


@user_router.message(Registration.grade, F.text)
async def process_grade(message: Message, state: FSMContext):
    grade = parse_grade(message.text)
    if grade is None:
        await message.answer("⚠️ Iltimos, 1 dan 11 gacha bo'lgan sinf raqamini kiriting.")
        return
    await state.update_data(grade=grade)
    await state.set_state(Registration.location)
    await message.answer(ASK_LOCATION)


@user_router.message(Registration.grade)
async def process_grade_invalid(message: Message):
    await message.answer("⚠️ Iltimos, sinf raqamini matn ko'rinishida yozing.")


@user_router.message(Registration.location, F.text)
async def process_location(message: Message, state: FSMContext):
    location = message.text.strip()
    if not is_valid_location(location):
        await message.answer("⚠️ Iltimos, hududingizni to'liqroq yozing.")
        return
    await state.update_data(location=location)
    await state.set_state(Registration.phone)
    await message.answer(ASK_PHONE, reply_markup=get_phone_keyboard())


@user_router.message(Registration.location)
async def process_location_invalid(message: Message):
    await message.answer("⚠️ Iltimos, manzilingizni matn ko'rinishida yozing.")


@user_router.message(Registration.phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext, bot: Bot):
    phone = message.contact.phone_number
    if not phone.startswith("+"):
        phone = "+" + phone
    await finish_registration(message, state, bot, phone)


@user_router.message(Registration.phone, F.text)
async def process_phone_text(message: Message, state: FSMContext, bot: Bot):
    phone = normalize_phone(message.text)
    if phone is None:
        await message.answer(
            "⚠️ Telefon raqam noto'g'ri. Masalan: +998901234567 ko'rinishida kiriting "
            "yoki pastdagi tugma orqali yuboring."
        )
        return
    await finish_registration(message, state, bot, phone)


@user_router.message(Registration.phone)
async def process_phone_invalid(message: Message):
    await message.answer("⚠️ Iltimos, telefon raqamingizni matn yoki kontakt orqali yuboring.")


async def finish_registration(message: Message, state: FSMContext, bot: Bot, phone: str):
    data = await state.get_data()
    full_name = f"{data['last_name']} {data['first_name']} {data['patronymic']}"
    reg_id = await add_registration(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        full_name=full_name,
        birth_date=data["birth_date"],
        grade=data["grade"],
        location=data["location"],
        phone=phone,
    )
    await state.clear()
    await message.answer(SUCCESS_TEXT, reply_markup=get_user_keyboard())
    await message.answer(
        "📣 <b>Do'stlaringizni ham tavsiya qiling!</b>\n\n"
        "Qadriyat Maktabini yaqinlaringizga ulashib, ularning ham "
        "sifatli ta'lim olishiga yordam bering! 🎓",
        reply_markup=get_share_keyboard(),
    )

    from database import format_dt, now_uzt
    admin_text = (
        f"🆕 <b>Yangi ariza #{reg_id}</b>\n\n"
        f"👤 <b>F.I.Sh:</b> {full_name}\n"
        f"🎂 <b>Tug'ilgan sana:</b> {data['birth_date']}\n"
        f"🏫 <b>Sinf:</b> {data['grade']}-sinf\n"
        f"📍 <b>Manzil:</b> {data['location']}\n"
        f"📞 <b>Telefon:</b> {phone}\n"
        f"🕐 <b>Vaqt:</b> {format_dt(now_uzt())}\n"
    )
    if message.from_user.username:
        admin_text += f"🔗 <b>Username:</b> @{message.from_user.username}\n"
    admin_text += f"🆔 <b>Telegram ID:</b> {message.from_user.id}"

    try:
        await bot.send_message(ADMIN_ID, "🔔")
        await bot.send_message(ADMIN_ID, admin_text)
    except Exception:
        logging.exception("Adminga xabar yuborib bo'lmadi")


# ───── Fallback ─────

@user_router.message()
async def fallback(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer(
            "Menyu uchun /start ni yuboring.",
            reply_markup=get_user_keyboard(),
        )
