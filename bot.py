import logging
import json
import os
from telegram import Update, WebAppInfo, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from order_queue import save_order, list_orders

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


async def handle_webapp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Receive data from WebApp and store the order."""
    try:
        data = json.loads(update.effective_message.web_app_data.data)
    except (ValueError, AttributeError):
        await update.message.reply_text('Не удалось обработать данные заказа.')
        return

    order = {
        'user_id': update.effective_user.id,
        'user_name': update.effective_user.full_name,
        'items': data,
    }
    save_order(order)
    await update.message.reply_text('Заказ получен и отправлен в обработку.')


async def orders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show list of user's orders."""
    orders = list_orders(update.effective_user.id)
    if not orders:
        await update.message.reply_text('У вас нет заказов.')
        return
    lines = []
    for o in orders:
        lines.append(f"\u2022 {o['created_at']}: {o['status']}")
    await update.message.reply_text('Ваши заказы:\n' + '\n'.join(lines))


def main():
    if not TOKEN:
        raise RuntimeError('TELEGRAM_TOKEN env required')
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('orders', orders))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp))
    app.run_polling()


if __name__ == '__main__':
    main()
