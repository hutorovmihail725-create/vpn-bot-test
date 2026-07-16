from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
import asyncio
import logging
import os
from aiohttp import web

logging.basicConfig(level=logging.INFO)

TOKEN = "8817790454:AAGbVx4-6IGIY0yhSW4rshgtI8aHiIhIfD4"
bot = Bot(token=TOKEN)
dp = Dispatcher()

WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = "https://vpn-bot-test-production.up.railway.app" + WEBHOOK_PATH

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Купить VPN", callback_data="buy_vpn")]
    ])
    await message.answer("Привет! Тестовый бот на Railway (Webhook).\nНажми кнопку:", reply_markup=keyboard)

@dp.callback_query(F.data == "buy_vpn")
async def buy_vpn(callback: types.CallbackQuery):
    await callback.answer("Работает!")
    await callback.message.answer("✅ Бот работает стабильно через Webhook!")

async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL)

async def main():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, lambda request: dp.feed_webhook_update(bot, await request.json()))
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    
    await on_startup(bot)
    print("Webhook бот запущен!")

if __name__ == "__main__":
    asyncio.run(main())
