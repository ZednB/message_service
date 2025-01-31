import logging

from aiogram import Bot
import asyncio
from telegram_bot.celery_config import celery_app

TOKEN = "7992641033:AAGoioDf-_-9b3MeBPqdMcqVd8LLXfqfzlw"
CHAT_ID = 1578231240

bot = Bot(token=TOKEN)
print(f"Бот с токеном {TOKEN} инициализирован.")


@celery_app.task(name="telegram_bot.tasks.send_telegram_message")
def send_telegram_message(text: str):
    print(f"Отправка сообщения в Telegram: {text}")
    try:
        # Используем asyncio.run() для асинхронной отправки сообщения
        loop = asyncio.get_event_loop()
        loop.run_until_complete(bot.send_message(chat_id=CHAT_ID, text=text))
        logging.info(f"Сообщение успешно отправлено в Telegram: {text}")
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения в Telegram: {e}")
