from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import logging
import os

logging.basicConfig(level=logging.INFO)
TOKEN = "7040599370:AAGToCNHmKWnLJswGAA4--y6fw7g9SMNXv0"
OWNER_ID = 7028050709  # استبدله برقمك

# خزن الرسائل اللي جت من المستخدمين: {owner_msg_id: sender_user_id}
msg_link = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلامٌ عليكم! تفضل بسؤالك أو اقتراحك 🌻")

async def anonymous_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    sent = await context.bot.send_message(chat_id=OWNER_ID, text=f"📩 رسالة مجهولة:\n\n{text}")
    msg_link[sent.message_id] = user_id

    await update.message.reply_text("✅ تم إرسال رسالتك بنجاح. شكراً!")

async def handle_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        original_msg_id = update.message.reply_to_message.message_id
        if original_msg_id in msg_link:
            target_user_id = msg_link[original_msg_id]
            reply_text = update.message.text

            await context.bot.send_message(chat_id=target_user_id, text=f"📝 رد من صاحب البوت:\n\n{reply_text}")
            await update.message.reply_text("✅ تم إرسال الرد.")
        else:
            await update.message.reply_text("❌ الرسالة الأصلية مش مربوطة بأي مستخدم، مش هقدر أبعتله.")
    else:
        await update.message.reply_text("❗ لازم تعمل Reply على رسالة علشان أعرف تبعتها لمين.")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.REPLY, anonymous_message))
    app.add_handler(MessageHandler(filters.TEXT & filters.REPLY, handle_reply))

    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
