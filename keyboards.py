from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


def get_phone_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def get_admin_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Statistika"), KeyboardButton(text="📥 Excel hisobot")],
            [KeyboardButton(text="📢 Xabar yuborish"), KeyboardButton(text="🗑️ Bazani tozalash")],
        ],
        resize_keyboard=True,
    )


def get_user_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Ro'yxatdan o'tish")],
            [KeyboardButton(text="📋 Mening arizalarim"), KeyboardButton(text="❓ Yordam")],
            [KeyboardButton(text="📍 Manzil"), KeyboardButton(text="💰 Narx va chegirmalar")],
            [KeyboardButton(text="❌ Ro'yxatdan o'tishni bekor qilish")],
        ],
        resize_keyboard=True,
    )


def get_status_keyboard(reg_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Qabul", callback_data=f"st_accepted_{reg_id}"),
        InlineKeyboardButton(text="🔄 Ko'rilmoqda", callback_data=f"st_review_{reg_id}"),
        InlineKeyboardButton(text="❌ Rad etildi", callback_data=f"st_rejected_{reg_id}"),
    ]])


def get_share_keyboard() -> InlineKeyboardMarkup:
    share_url = (
        "https://t.me/share/url"
        "?url=https%3A%2F%2Ft.me%2Fqadriyat_school_qabulbot"
        "&text=Qadriyat+Xususiy+Maktabi+%E2%80%94+Farg%27ona+viloyatidagi+eng+yaxshi+ta%27lim!"
        "+%F0%9F%8E%93+Men+ham+ro%27yxatdan+o%27tdim.+Siz+ham+qo%27shiling!"
    )
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📣 Do'stingizga tavsiya qiling", url=share_url)]
    ])


def get_reset_confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Ha, o'chir", callback_data="reset_confirm"),
            InlineKeyboardButton(text="❌ Bekor qil", callback_data="reset_cancel"),
        ]
    ])
