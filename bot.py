import asyncio
import json
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup

# ============ НАСТРОЙКИ — ЗАПОЛНИ ЭТИ 3 СТРОЧКИ ============
BOT_TOKEN = "8723612144:AAEMMQDQty8BTVwOqgXzlZ1SBo5W4TAd6UI"
WEBAPP_URL = "https://8hm96gpkb9-crypto.github.io/garage/"
OWNER_CHAT_ID = 280074884  # твой личный chat_id (число), см. README как узнать
# =============================================================

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
