import logging
from pathlib import Path

from aiohttp import web

from config import ADMIN_ID
from database import add_registration
from validators import (
    is_valid_full_name,
    is_valid_location,
    normalize_phone,
    parse_grade,
)

WEBSITE_DIR = Path(__file__).parent / "website"

PAGE_NAMES = {"index", "biz-haqimizda", "talim", "sharoitlar"}

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}


async def api_register_options(request: web.Request) -> web.Response:
    return web.Response(headers=CORS_HEADERS)


async def serve_index(request: web.Request) -> web.Response:
    return web.FileResponse(WEBSITE_DIR / "index.html")


async def serve_page(request: web.Request) -> web.Response:
    name = request.match_info["page"]
    if name not in PAGE_NAMES:
        raise web.HTTPNotFound()
    return web.FileResponse(WEBSITE_DIR / f"{name}.html")


async def api_register(request: web.Request) -> web.Response:
    try:
        data = await request.json()
    except ValueError:
        return web.json_response(
            {"ok": False, "errors": {"form": "Noto'g'ri so'rov formati."}},
            status=400,
            headers=CORS_HEADERS,
        )

    errors = {}

    full_name = str(data.get("full_name", "")).strip()
    if not is_valid_full_name(full_name):
        errors["full_name"] = (
            "F.I.Sh.ni to'liq va faqat harflar bilan kiriting (2-100 belgi)."
        )

    phone = normalize_phone(str(data.get("phone", "")))
    if phone is None:
        errors["phone"] = "Telefon raqam noto'g'ri. Masalan: +998901234567."

    grade = parse_grade(str(data.get("grade", "")))
    if grade is None:
        errors["grade"] = "Sinfni 1 dan 11 gacha tanlang."

    location = str(data.get("location", "")).strip()
    if not is_valid_location(location):
        errors["location"] = "Manzilingizni to'liqroq yozing."

    if errors:
        return web.json_response({"ok": False, "errors": errors}, headers=CORS_HEADERS)

    reg_id = await add_registration(
        telegram_id=0,
        username="web",
        full_name=full_name,
        birth_date="-",
        grade=grade,
        location=location,
        phone=phone,
    )

    admin_text = (
        f"🌐 <b>Veb-sayt orqali yangi ariza #{reg_id}</b>\n\n"
        f"👤 <b>F.I.Sh:</b> {full_name}\n"
        f"🏫 <b>Sinf:</b> {grade}-sinf\n"
        f"📍 <b>Manzil:</b> {location}\n"
        f"📞 <b>Telefon:</b> {phone}\n"
    )

    bot = request.app.get("bot")
    if bot is not None:
        try:
            await bot.send_message(ADMIN_ID, admin_text)
        except Exception:
            logging.exception("Adminga veb-sayt arizasi haqida xabar yuborib bo'lmadi")

    return web.json_response({"ok": True}, headers=CORS_HEADERS)


def setup_website_routes(app: web.Application) -> None:
    app.router.add_post("/api/register", api_register)
    app.router.add_route("OPTIONS", "/api/register", api_register_options)
    app.router.add_get("/", serve_index)
    app.router.add_get("/{page}.html", serve_page)
    app.router.add_static("/assets", WEBSITE_DIR / "assets")
