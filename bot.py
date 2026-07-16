from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

import os
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Купить VPN", callback_data="buy_vpn")]
    ])
    await message.answer("Привет! Тестовый бот.", reply_markup=keyboard)

@dp.callback_query(F.data == "buy_vpn")
async def buy_vpn(callback: types.CallbackQuery):
    await callback.answer("Бот работает!")
    await callback.message.answer("✅ Всё работает!")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
