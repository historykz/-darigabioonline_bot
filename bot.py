from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = "ВСТАВЬ_НОВЫЙ_TOKEN"
ADMIN_ID = 123456789

user_map = {}

async def handle_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    msg = await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Новое сообщение\n\nИмя: {user.full_name}\nUsername: @{user.username}\nID: {user.id}\n\n{text}"
    )

    user_map[msg.message_id] = user.id

async def handle_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        msg_id = update.message.reply_to_message.message_id
        if msg_id in user_map:
            await context.bot.send_message(
                chat_id=user_map[msg_id],
                text=update.message.text
            )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.User(ADMIN_ID), handle_user))
app.add_handler(MessageHandler(filters.TEXT & filters.User(ADMIN_ID), handle_admin))

app.run_polling()
