# Qadriyat School — Ro'yxatga olish boti

Qadriyat maktabiga o'qishga qabul qilish uchun ariza qabul qiluvchi Telegram bot.

## 🧩 Bot nima qiladi

### Oddiy foydalanuvchi uchun
1. `/start` bosilganda bot o'zini tanishtiradi va "📝 Ro'yxatdan o'tish" tugmasini chiqaradi.
2. Tugma bosilgach, ketma-ket so'raladi:
   - To'liq ism-sharif (Familiya Ism)
   - Tug'ilgan sana (kun.oy.yil, masalan 15.03.2012)
   - Nechanchi sinfga kirmoqchi (1–11)
   - Qaysi hudud / tuman / shahardan
   - Telefon raqam (tugma orqali yuborish yoki qo'lda yozish)
3. Hammasi to'g'ri kiritilgach: "✅ Arizangiz qabul qilindi! Tez orada operatorlarimiz siz bilan bog'lanishadi."
4. Har bir yangi ariza darhol adminga (sizga) xabar qilinadi.
5. Istalgan vaqtda `/bekor` buyrug'i bilan jarayonni bekor qilish mumkin.
6. Har bir bosqichda noto'g'ri ma'lumot kiritilsa, bot xato bermaydi — shunchaki qaytadan so'raydi.

### Admin uchun (Telegram ID: 8104665298)
`/start` bosilganda boshqaruv paneli ochiladi:
- 📊 **Statistika** — jami va bugungi arizalar soni
- 📥 **Excel hisobot** — barcha arizalarni `.xlsx` faylda yuboradi

Excel fayl ustunlari: **№, F.I.Sh., Tug'ilgan sana, Sinf, Manzil, Telefon raqam, Ro'yxatdan o'tgan sana**.

Hisobot bazadan jonli (real-time) generatsiya qilinadi, shuning uchun har safar "📥 Excel hisobot"
tugmasi bosilganda eng so'nggi ma'lumotlar bilan fayl yuboriladi.

## ⚙️ O'rnatish

1. Python 3.10+ kerak (tekshirish: `python3 --version`).
2. Loyiha papkasiga kiring:
   ```bash
   cd ~/Desktop/qadriyat_school_bot
   ```
3. Virtual muhit yaratish (tavsiya etiladi):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Kerakli kutubxonalarni o'rnatish:
   ```bash
   pip install -r requirements.txt
   ```
5. `.env` faylini yaratish:
   ```bash
   cp .env.example .env
   ```
   Uni ochib, bot tokeningizni yozing:
   ```
   BOT_TOKEN=123456789:AAExampleTokenHere
   ADMIN_ID=8104665298
   ```

## ▶️ Ishga tushirish

```bash
python bot.py
```

Konsolda xatosiz ishga tushgandan so'ng, Telegramda botingizga `/start` yuborib sinab ko'rishingiz mumkin.

⚠️ **Muhim:** Bot sizga (admin) avtomatik xabarlar va Excel hisobot yubora olishi uchun
**avval o'zingiz botga `/start` yuborishingiz kerak** — Telegram bot tomonidan
boshlanmagan suhbatga xabar yuborishga ruxsat bermaydi.

## ☁️ Render'ga joylashtirish (bepul, kompyuter o'chsa ham ishlaydi)

1. Loyihani GitHub repositoryga yuklang (push qiling).
2. [render.com](https://render.com) da ro'yxatdan o'ting va GitHub akkauntingizni ulang.
3. **New +** → **Blueprint** ni tanlang va shu repositoryni tanlang
   (loyihada `render.yaml` fayli bor, Render uni avtomatik o'qiydi).
4. Render so'raganda quyidagi environment variable'larni kiriting:
   - `BOT_TOKEN` — bot tokeningiz
   - `ADMIN_ID` — admin Telegram ID
5. **Apply/Deploy** tugmasini bosing. Bir necha daqiqadan so'ng bot ishga tushadi.

⚠️ **Eslatma (bepul reja uchun):**
- Bepul "Web Service" 15 daqiqa faoliyatsizlikdan keyin "uxlab qoladi". Botni 24/7
  uyg'oq ushlab turish uchun [cron-job.org](https://cron-job.org) yoki
  [UptimeRobot](https://uptimerobot.com) kabi xizmat orqali Render bergan URL
  manzilingizga har 10 daqiqada so'rov yuborib turing.
- `registrations.db` fayli serverning vaqtinchalik diskida saqlanadi — Render
  qayta deploy qilinganda yoki uxlab-uyg'onganda bu fayl **o'chib ketishi mumkin**.
  Doimiy saqlash kerak bo'lsa, Render'ning pullik "Persistent Disk" yoki
  tashqi ma'lumotlar bazasidan (masalan, PostgreSQL) foydalanish tavsiya etiladi.

## 🖥️ Serverga doimiy joylashtirish (systemd)

1. Loyiha papkasini serverga ko'chiring va yuqoridagi o'rnatish qadamlarini bajaring
   (venv yaratish, kutubxonalarni o'rnatish, `.env` ni to'ldirish).
2. `qadriyat-bot.service` faylidagi `User`, `WorkingDirectory` va `ExecStart`
   yo'llarini o'zingizning server tuzilmangizga moslang.
3. Faylni systemd papkasiga nusxalang va xizmatni ishga tushiring:
   ```bash
   sudo cp qadriyat-bot.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable --now qadriyat-bot
   ```
4. Holatini tekshirish va loglarni ko'rish:
   ```bash
   sudo systemctl status qadriyat-bot
   journalctl -u qadriyat-bot -f
   ```

Bu bot kompyuter/server qayta yoqilganda ham avtomatik ishga tushadi va
yiqilib qolsa (xatolik bo'lsa) avtomatik qayta ishga tushadi (`Restart=always`).

## 📁 Fayl tuzilishi

```
qadriyat_school_bot/
├── bot.py              # botni ishga tushiruvchi asosiy fayl
├── config.py           # token va admin ID ni .env dan o'qiydi
├── database.py         # SQLite bilan ishlash (registrations.db)
├── excel_export.py     # Excel hisobot generatsiyasi
├── states.py           # ro'yxatdan o'tish bosqichlari (FSM)
├── validators.py        # kiritilgan ma'lumotlarni tekshirish
├── keyboards.py         # tugmalar
├── handlers/
│   ├── user.py          # foydalanuvchi oqimi
│   └── admin.py         # admin paneli
├── requirements.txt
├── .env.example
└── qadriyat-bot.service # systemd shabloni
```

Barcha ro'yxatdan o'tganlar `registrations.db` (SQLite) faylida saqlanadi —
bu fayl `python bot.py` birinchi marta ishga tushirilganda avtomatik yaratiladi.
