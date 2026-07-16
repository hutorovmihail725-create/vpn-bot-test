from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

TOKEN = "8817790454:AAGbVx4-6IGIY0yhSW4rshgtI8aHiIhIfD4"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Купить VPN", callback_data="buy_vpn")]
    ])
    await message.answer("Привет! Это тестовый VPN бот.\nНажми кнопку:", reply_markup=keyboard)

@dp.callback_query(F.data == "buy_vpn")
async def buy_vpn(callback: types.CallbackQuery):
    await callback.answer("Работает!")
    await callback.message.answer("✅ Бот на Railway работает!")

async def main():
    print("Бот запущен на Railway!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
