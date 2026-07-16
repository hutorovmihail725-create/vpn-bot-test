from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
import asyncio
import logging
import os
import sqlite3
import datetime
import random
import string

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- БАЗА ДАННЫХ ---
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            vpn_config TEXT,
            subscription_until TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_user_subscription(user_id, config_link):
    expires_at = (datetime.datetime.now() + datetime.timedelta(days=30)).isoformat()
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (user_id, vpn_config, subscription_until) 
        VALUES (?, ?, ?) 
        ON CONFLICT(user_id) DO UPDATE SET 
            vpn_config = excluded.vpn_config, 
            subscription_until = excluded.subscription_until
    ''', (user_id, config_link, expires_at))
    conn.commit()
    conn.close()

# --- ГЕНЕРАЦИЯ ФЕЙКОВОГО КОНФИГА ---
def create_vpn_user_on_server():
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    return f"vless://test-user-{random_string}@your-vps-ip:443?security=reality&sni=microsoft.com#VPN"

# --- КНОПКА БЕЗ ОПЛАТЫ ДЛЯ ТЕСТА ---
@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="💳 Купить VPN (ТЕСТ БЕЗ ОПЛАТЫ)", callback_data="buy_vpn")]
    ])
    await message.answer(
        "🛠️ РЕЖИМ ТЕСТА БЕЗ ОПЛАТЫ.\n\n"
        "Нажми кнопку, чтобы мгновенно получить тестовый конфиг и проверить работу базы данных.",
        reply_markup=keyboard
    )

@dp.callback_query(F.data == "buy_vpn")
async def buy_vpn(callback: types.CallbackQuery):
    await callback.answer("Генерирую конфиг...")
    
    user_id = callback.from_user.id
    config_link = create_vpn_user_on_server()
    save_user_subscription(user_id, config_link)
    
    await callback.message.answer(
        f"✅ ТЕСТОВАЯ ПОДПИСКА АКТИВИРОВАНА (на 30 дней)!\n\n"
        f"**Ссылка для подключения:**\n"
        f"`{config_link}`\n\n"
        f"📅 База данных сохранила запись. Теперь ты готов к подключению реальной оплаты.",
        parse_mode="Markdown"
    )

async def main():
    init_db()
    print("Бот в режиме теста БЕЗ ОПЛАТЫ запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
