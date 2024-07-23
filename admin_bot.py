from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

user_status = {}
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("🔒 Akun diblokir", callback_data='akun_diblokir')],
        [InlineKeyboardButton("🔑 Tidak bisa login", callback_data='tidak_bisa_login')],
        [InlineKeyboardButton("🔐 Lupa kata sandi", callback_data='lupa_kata_sandi')],
        [InlineKeyboardButton("💬 Live Agent", callback_data='live_agent')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_text('Silakan pilih masalah yang Anda alami:', reply_markup=reply_markup)
    elif update.callback_query:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Silakan pilih masalah yang Anda alami:', reply_markup=reply_markup)

async def show_back_and_cancel_buttons(query):
    keyboard = [
        [InlineKeyboardButton("🔙 Kembali", callback_data='kembali')],
        [InlineKeyboardButton("❌ Batal", callback_data='batal')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_reply_markup(reply_markup=reply_markup)

async def show_cancel_button(query):
    keyboard = [
        [InlineKeyboardButton("❌ Batal", callback_data='batal')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_reply_markup(reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data in ['akun_diblokir', 'tidak_bisa_login', 'lupa_kata_sandi']:
        if query.data == 'akun_diblokir':
            response_message = "Pilih opsi chat dengan admin."
        elif query.data == 'tidak_bisa_login':
            response_message = "Silahkan daftar terlebih dahulu."
        elif query.data == 'lupa_kata_sandi':
            response_message = "Anda bisa reset melalui website https://www.warsa.online/assets/reset"

        await query.edit_message_text(text=response_message)
        await show_back_and_cancel_buttons(query)
    elif query.data == 'live_agent':
        response_message = "Anda akan terhubung dengan developer. Silahkan tulis masalah anda."
        await query.edit_message_text(text=response_message)
        await show_cancel_button(query)  
        user_status[update.effective_user.id] = 'live_agent'
    elif query.data == 'kembali':
        await query.edit_message_text(
            text='Silakan pilih masalah yang Anda alami:',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔒 Akun diblokir", callback_data='akun_diblokir')],
                [InlineKeyboardButton("🔑 Tidak bisa login", callback_data='tidak_bisa_login')],
                [InlineKeyboardButton("🔐 Lupa kata sandi", callback_data='lupa_kata_sandi')],
                [InlineKeyboardButton("💬 Chat dengan admin", callback_data='live_agent')]
            ])
        )
        user_status.pop(update.effective_user.id, None)  
    elif query.data == 'batal':
        await query.edit_message_text(text="Operasi dibatalkan.")
        user_status.pop(update.effective_user.id, None) 

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id in user_status and user_status[user_id] == 'live_agent':
        owner_id = '6796173678' 
        if 'message_sent' not in user_status[user_id]:
            await context.bot.send_message(chat_id=owner_id, text=f"Pesan dari pengguna {user_id}: {update.message.text}")
            user_status[user_id]['message_sent'] = True
        await update.message.reply_text("Pesan Anda telah dikirim ke developer.")
    elif update.effective_chat.id == int('6796173678'):
        for user_id in user_status:
            if user_status[user_id] == 'live_agent':
                await context.bot.send_message(chat_id=user_id, text=update.message.text)
                await update.message.reply_text("Pesan Anda telah dikirim ke pengguna.")

def main() -> None:
    application = ApplicationBuilder().token("6874519471:AAHu_ffn3BFMk-vx4X3V8H45tV-hWVS272M").build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == '__main__':
    main()
