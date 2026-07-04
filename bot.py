import asyncio
import json
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup

# ============ НАСТРОЙКИ ============
# Токен и остальные данные теперь берутся из переменных окружения,
# а не из кода — так они не попадут в репозиторий на GitHub.
BOT_TOKEN = os.environ["BOT_TOKEN"]
WEBAPP_URL = os.environ["WEBAPP_URL"]
OWNER_CHAT_ID = int(os.environ.get("OWNER_CHAT_ID", "0"))
# =====================================

logging.basicConfig(level=logging.INFO)
bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[
            KeyboardButton(text="🛍 Открыть каталог", web_app=WebAppInfo(url=WEBAPP_URL))
        ]],
        resize_keyboard=True
    )
    await message.answer(
        "Привет! Здесь можно посмотреть вещи, которые я продаю.\n"
        "Нажми кнопку ниже, чтобы открыть каталог 👇",
        reply_markup=kb
    )


@dp.message(F.web_app_data)
async def handle_web_app_data(message: Message):
    """Срабатывает, когда покупатель нажал «Забронировать» в мини-приложении."""
    try:
        data = json.loads(message.web_app_data.data)
    except (json.JSONDecodeError, AttributeError):
        return

    user = message.from_user
    contact = f"@{user.username}" if user.username else user.full_name

    text = (
        "📦 Новая заявка на бронь!\n\n"
        f"Товар: {data.get('name', '—')}\n"
        f"Цена: {data.get('price', '—')}\n"
        f"№ товара: {data.get('id', '—')}\n\n"
        f"От кого: {contact}\n"
        f"Написать: tg://user?id={user.id}"
    )

    if OWNER_CHAT_ID:
        await bot.send_message(OWNER_CHAT_ID, text)

    await message.answer(
        f"Вы забронировали: «{data.get('name', '—')}» за {data.get('price', '—')}.\n"
        "Заявка отправлена продавцу, он скоро с вами свяжется 🙌"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
