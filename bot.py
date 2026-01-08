from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

import os

TOKEN = os.getenv("8446176699:AAERBCaANUfPIkDw0jV7dKwvUNqLgtb5jKM")
ADMIN_ID = int(os.getenv("6970052867"))


# ====== XOTIRA ======
user_coin_order = {}

# ================== START ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text="✅ TEST: Bot adminga yoza oladi"
    )

    keyboard = [
        ["🪙 Coin sotib olish"],
        ["🎁 Yutib olish", "👤 Shaxsiy kabinet"],
        ["💼 Akkaunt sotib olish", "✅ Ishonchli kanallar"],
        ["📞 Admin bilan bog‘lanish"]
    ]
    await update.message.reply_text(
        "🚗 CPM 1 savdo botiga xush kelibsiz!",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# ================== COIN ==================
async def coin_sotib_olish(update, context):
    keyboard = [
        ["10000 coin - 10000 so'm"],
        ["20000 coin - 12000 so'm"],
        ["30000 coin - 13000 so'm"],
        ["100000 coin - 15000 so'm"],
        ["500000 coin - 17000 so'm"],
        ["50 mln pul - 8000 so'm"]
    ]
    await update.message.reply_text(
        "Qancha miqdorda coin sotib olmoqchsiz?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

COIN_PACKETS = [
    "10000 coin - 10000 so'm",
    "20000 coin - 12000 so'm",
    "30000 coin - 13000 so'm",
    "100000 coin - 15000 so'm",
    "500000 coin - 17000 so'm",
    "50 mln pul - 8000 so'm"
]

async def coin_buyurtma(update, context):
    user = update.message.from_user
    user_coin_order[user.id] = update.message.text

    await update.message.reply_text(
        "Buyurtma qabul qilindi ✅\n\n"
        "Endi @eagle1card shu kanalda berilgan kartaga\n"
        "ko‘rsatilgan summani o‘tkazib,\n"
        "to‘lov chekini yuboring.\n\n"
        "Adminlar sizga aloqaga chiqishadi."
    )

async def coin_chek_qabul(update, context):
    user = update.message.from_user

    if user.id not in user_coin_order:
        await update.message.reply_text(
            "❗ Avval coin paket tanlashingiz kerak."
        )
        return

    username = user.username or "username yo‘q"
    paket = user_coin_order[user.id]

    caption = (
        "🪙 COIN BUYURTMA CHEKI\n\n"
        f"👤 @{username}\n"
        f"🆔 ID: {user.id}\n"
        f"📦 Paket: {paket}"
    )

    # Agar rasm bo‘lsa
    if update.message.photo:
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=update.message.photo[-1].file_id,
            caption=caption
        )

    # Agar fayl (PDF va boshqalar) bo‘lsa
    elif update.message.document:
        await context.bot.send_document(
            chat_id=ADMIN_ID,
            document=update.message.document.file_id,
            caption=caption
        )

    await update.message.reply_text(
        "Chek yuborildi ✅\nAdmin tekshiradi va siz bilan bog‘lanadi."
    )

    del user_coin_order[user.id]

# ================== BOSHQA BO‘LIMLAR ==================
async def yutib_olish(update, context):
    await update.message.reply_text(
        "Ishonchli kanallarda har hafta konkurslar bo‘ladi,\n"
        "ularda qatnashib har xil yutuqlar yutib olishingiz mumkin 🎉"
    )

async def shaxsiy_kabinet(update, context):
    user = update.message.from_user
    username = user.username or "username yo‘q"
    await update.message.reply_text(
        "👤 Shaxsiy kabinet\n\n"
        f"👤 Username: @{username}\n"
        "📦 Buyurtmalar: 0"
    )

async def akkaunt_sotib_olish(update, context):
    keyboard = [
        ["🔐 Full akkount"],
        ["✍️ Siz xohlagandek akkount"]
    ]
    await update.message.reply_text(
        "Qanday akkount sotib olmoqchisiz?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def full_akkaunt(update, context):
    await update.message.reply_text(
        "Full akkount haqida va narxini\n"
        "https://t.me/cpmsavdo88/79\n\n"
        "Sizga ma’qul kelsa @eaglecpm bilan bog‘laning."
    )

async def ishonchli_kanallar(update, context):
    await update.message.reply_text(
        "Hozircha kanalimiz 1 ta 👇\n\n👉 @cpmsavdo88"
    )

async def admin_bilan_boglanish(update, context):
    await update.message.reply_text(
        "Bot yaratuvchisi va kanal egasi: @eaglecpm\n\n"
        "Muammo yoki taklif bo‘lsa shu yerga yozing."
    )

# ================== APP ==================
app = ApplicationBuilder().token(TOKEN).build()

# 🔴 PHOTO ENG YUQORIDA TURISHI SHART
app.add_handler(
    MessageHandler(filters.PHOTO | filters.Document.ALL, coin_chek_qabul)
)


app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Text("🪙 Coin sotib olish"), coin_sotib_olish))
app.add_handler(MessageHandler(filters.Text(COIN_PACKETS), coin_buyurtma))
app.add_handler(MessageHandler(filters.Text("🎁 Yutib olish"), yutib_olish))
app.add_handler(MessageHandler(filters.Text("👤 Shaxsiy kabinet"), shaxsiy_kabinet))
app.add_handler(MessageHandler(filters.Text("💼 Akkaunt sotib olish"), akkaunt_sotib_olish))
app.add_handler(MessageHandler(filters.Text("🔐 Full akkount"), full_akkaunt))
app.add_handler(MessageHandler(filters.Text("✅ Ishonchli kanallar"), ishonchli_kanallar))
app.add_handler(MessageHandler(filters.Text("📞 Admin bilan bog‘lanish"), admin_bilan_boglanish))

print("✅ CPM 1 bot ishga tushdi...")
app.run_polling()

