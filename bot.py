import logging
from telegram import Update, WebAppInfo, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://example.com')

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    text = f"Привет, {user.first_name}!"\
           "\nДля оформления заказа откройте мини-приложение."
    keyboard = [[{
        'text': 'Открыть магазин',
        'web_app': WebAppInfo(url=WEBAPP_URL)
    }]]
    await update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))


def main():
    if not TOKEN:
        raise RuntimeError('TELEGRAM_TOKEN env required')
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.run_polling()


if __name__ == '__main__':
    main()
