from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from telegram.ext import filters
import os, logging

logging.basicConfig(level=logging.INFO)
TOKEN = "7040599370:AAGToCNHmKWnLJswGAA4--y6fw7g9SMNXv0"  # توكن البوت
OWNER_ID = 7028050709             # غيره لـ ID بتاعك

# خزن الرسائل اللي جت من المستخدمين: {owner_msg_id: sender_user_id}
msg_link = {}

def start(update: Update, context: CallbackContext):
    update.message.reply_text("سلامٌ عليكم! تفضل بسؤالك أو اقتراحك 🌻")

def anonymous_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    text = update.message.text

    # ابعت الرسالة لصاحب البوت
    sent = context.bot.send_message(chat_id=OWNER_ID, text=f"📩 رسالة مجهولة:\n\n{text}")

    # اربط رقم الرسالة اللي اتبعتتلك بصاحبها
    msg_link[sent.message_id] = user_id

    # رد للمستخدم
    update.message.reply_text("✅ تم إرسال رسالتك بنجاح. شكراً!")

def handle_reply(update: Update, context: CallbackContext):
    if update.message.reply_to_message:
        original_msg_id = update.message.reply_to_message.message_id

        if original_msg_id in msg_link:
            target_user_id = msg_link[original_msg_id]
            reply_text = update.message.text

            # ابعت الرد للمستخدم المجهول
            context.bot.send_message(chat_id=target_user_id, text=f"📝 رد من صاحب البوت:\n\n{reply_text}")
            update.message.reply_text("✅ تم إرسال الرد.")
        else:
            update.message.reply_text("❌ الرسالة الأصلية مش مربوطة بأي مستخدم، مش هقدر أبعتله.")
    else:
        update.message.reply_text("❗ لازم تعمل Reply على رسالة علشان أعرف تبعتها لمين.")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.REPLY, anonymous_message))  # تعديل هنا
    dp.add_handler(MessageHandler(filters.TEXT & filters.REPLY, handle_reply))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
