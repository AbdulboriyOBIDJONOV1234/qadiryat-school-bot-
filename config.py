import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8104665298"))

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN topilmadi! '.env' faylini yarating (.env.example dan nusxa "
        "oling) va unga BOT_TOKEN=... qatorini qo'shing."
    )
