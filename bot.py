from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

TOKEN = "8817790454:AAGbVx4-6IGIY0yhSW4rshgtI8aHiIhIfD4"

PROXY = "http://170.81.131.70:3128"

bot = Bot(token=TOKEN, proxy=PROXY)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Бот с прокси.")

@dp.callback_query()
async def callback_handler(callback: types.CallbackQuery):
    await callback.answer("Бот работает!")

async def main():
    print("Бот запущен с прокси...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
