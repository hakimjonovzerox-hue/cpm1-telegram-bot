import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# ================== SOZLAMALAR ==================

TOKEN = "8446176699:AAERBCaANUfPIkDw0jV7dKwvUNqLgtb5jKM"
ADMIN_ID = 6970052867  # Admin ID

# ================== MENYULAR ==================
USERNAME_MENU = ReplyKeyboardMarkup(
    [["✅ Username qo‘ydim"]],
    resize_keyboard=True
)


MAIN_MENU = ReplyKeyboardMarkup(
    [
        ["🛒 Coin sotib olish", "🎁 Yutib olish"],
        ["👤 Shaxsiy kabinet", "🛍 Akkount sotib olish"],
        ["📢 Ishonchli kanallar", "📞 Admin bilan bog'lanish"],
    ],
    resize_keyboard=True
)

BACK_MENU = ReplyKeyboardMarkup([["🔙 Menyuga qaytish"]], resize_keyboard=True)

USERNAME_MENU = ReplyKeyboardMarkup([["✅ Username qo‘ydim"]], resize_keyboard=True)

ACCOUNT_MENU = ReplyKeyboardMarkup(
    [
        ["✅ Full akkount", "✍️ Siz xohlagandek akkount"],
        ["🔙 Menyuga qaytish"]
    ],
    resize_keyboard=True
)

COIN_MENU = ReplyKeyboardMarkup(
    [
        ["10000 coin - 10000 so'm", "20000 coin - 12000 so'm"],
        ["30000 coin - 13000 so'm", "100000 coin - 15000 so'm"],
        ["500000 coin - 17000 so'm", "50 mln pul - 8000 so'm"],
        ["🔙 Menyuga qaytish"]
    ],
    resize_keyboard=True
)

# ================== START ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Asosiy menyu:", reply_markup=MAIN_MENU)

async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("Asosiy menyuga qaytdingiz.", reply_markup=MAIN_MENU)

# ================== COIN ==================

async def coin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Qancha miqdorda coin olasiz?", reply_markup=COIN_MENU)

async def coin_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["waiting_payment"] = True
    context.user_data["order_text"] = update.message.text

    await update.message.reply_text(
        "Buyurtma qabul qilindi.\n\n"
        "To‘lovni qilib, CHEKNI yuboring.",
        reply_markup=BACK_MENU
    )

# ================== CHEK QABUL QILISH ==================
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("waiting_payment"):
        return

    user = update.message.from_user
    photo_id = update.message.photo[-1].file_id

    context.user_data["pending_photo"] = photo_id

    if not user.username:
        await context.bot.send_photo(
            chat_id=update.message.chat_id,
            photo=open("username_required.jpg", "rb"),
            caption="❗ Iltimos, buyurtmangiz adminga yuborilishi uchun profilingizga username qo‘ying.",
            reply_markup=USERNAME_MENU
        )
        return

    await send_to_admin(update, context, user.username)


# ================== USERNAME TEKSHIRISH ==================

async def check_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    if not user.username:
        await update.message.reply_text(
            "❌ Siz hali username qo‘ymadingiz.",
            reply_markup=USERNAME_MENU
        )
        return

    await send_to_admin(update, context)

# ================== ADMINGA YUBORISH ==================

async def send_to_admin(update, context, username):
    order = context.user_data.get("order_text", "Buyurtma aniqlanmadi")
    photo = context.user_data.get("pending_photo")

    if not photo:
        await update.message.reply_text("❌ Chek topilmadi. Qaytadan yuboring.")
        return

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo,
        caption=(
            "💳 YANGI TO‘LOV CHEKI\n\n"
            f"👤 Foydalanuvchi: @{username}\n"
            f"🛒 Buyurtma: {order}\n\n"
            "Tekshirib tasdiqlang."
        )
    )

    context.user_data.clear()

    await update.message.reply_text(
        "✅ To‘lov qabul qilindi. Admin tekshiradi.",
        reply_markup=MAIN_MENU
    )

# ================== BOSHQA FUNKSIYALAR ==================

async def win_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Konkurslar kanallarda bo‘ladi.", reply_markup=BACK_MENU)

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    username = user.username or "Yo‘q"
    await update.message.reply_text(f"Username: @{username}", reply_markup=BACK_MENU)

async def account_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Qanday akkount?", reply_markup=ACCOUNT_MENU)

async def full_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("https://t.me/cpmsavdo88/79", reply_markup=BACK_MENU)

async def custom_account_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["waiting_custom_account"] = True
    await update.message.reply_text("Talabingizni yozing:", reply_markup=BACK_MENU)

async def contact_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["waiting_admin_message"] = True
    await update.message.reply_text("Xabaringizni yozing:", reply_markup=BACK_MENU)

async def trusted_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("@cpmsavdo88", reply_markup=BACK_MENU)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.from_user

    if context.user_data.get("waiting_custom_account"):
        await context.bot.send_message(ADMIN_ID, f"Custom akkount:\n@{user.username}\n{text}")
        context.user_data.clear()
        await update.message.reply_text("Yuborildi.", reply_markup=MAIN_MENU)

    elif context.user_data.get("waiting_admin_message"):
        await context.bot.send_message(ADMIN_ID, f"Xabar:\n@{user.username}\n{text}")
        context.user_data.clear()
        await update.message.reply_text("Yuborildi.", reply_markup=MAIN_MENU)
async def send_to_admin(update, context, username):
    order = context.user_data.get("order_text", "Buyurtma aniqlanmadi")
    photo = update.message.photo[-1].file_id

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo,
        caption=(
            "💳 YANGI TO‘LOV CHEKI\n\n"
            f"👤 Foydalanuvchi: @{username}\n"
            f"🛒 Buyurtma: {order}\n\n"
            "Tekshirib tasdiqlang."
        )
    )

    context.user_data["waiting_payment"] = False

    await update.message.reply_text(
        "✅ To‘lov qabul qilindi.\nAdmin tekshiradi.",
        reply_markup=MAIN_MENU
    )
async def check_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    if not user.username:
        await update.message.reply_text(
            "❌ Siz hali username qo‘ymadingiz.",
            reply_markup=USERNAME_MENU
        )
        return

    await send_to_admin(update, context, user.username)

# ================== ISHGA TUSHIRISH ==================

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.Regex("✅ Username qo‘ydim"), check_username))

    app.add_handler(MessageHandler(filters.Regex("🔙 Menyuga qaytish"), back_to_menu))
    app.add_handler(MessageHandler(filters.Regex("🛒 Coin sotib olish"), coin_menu))
    app.add_handler(MessageHandler(filters.Regex("coin"), coin_order))
    app.add_handler(MessageHandler(filters.Regex("🎁 Yutib olish"), win_info))
    app.add_handler(MessageHandler(filters.Regex("👤 Shaxsiy kabinet"), profile))
    app.add_handler(MessageHandler(filters.Regex("🛍 Akkount sotib olish"), account_menu))
    app.add_handler(MessageHandler(filters.Regex("✅ Full akkount"), full_account))
    app.add_handler(MessageHandler(filters.Regex("✍️ Siz xohlagandek akkount"), custom_account_request))
    app.add_handler(MessageHandler(filters.Regex("📢 Ishonchli kanallar"), trusted_channels))
    app.add_handler(MessageHandler(filters.Regex("📞 Admin bilan bog'lanish"), contact_admin))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.Regex("Username qo‘ydim"), check_username))


    app.run_polling()

if __name__ == "__main__":
    main()
