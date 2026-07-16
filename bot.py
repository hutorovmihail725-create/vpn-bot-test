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

# --- 1. НАСТРОЙКА БАЗЫ ДАННЫХ (SQLite) ---
# Создает файл database.db, если его нет
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Создаем таблицу пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            vpn_config TEXT,
            subscription_until TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Функция для сохранения подписки в БД
def save_user_subscription(user_id, config_link):
    expires_at = (datetime.datetime.now() + datetime.timedelta(days=30)).isoformat()
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Если пользователь уже есть, обновляем. Если нет - создаем
    cursor.execute('''
        INSERT INTO users (user_id, vpn_config, subscription_until) 
        VALUES (?, ?, ?) 
        ON CONFLICT(user_id) DO UPDATE SET 
            vpn_config = excluded.vpn_config, 
            subscription_until = excluded.subscription_until
    ''', (user_id, config_link, expires_at))
    conn.commit()
    conn.close()

# --- 2. ФУНКЦИЯ СОЗДАНИЯ VPN (ЗАГЛУШКА ДЛЯ ТЕСТА) ---
# Когда купишь VPS, мы просто заменим код внутри этой функции на запрос к 3X-UI
def create_vpn_user_on_server():
    # Генерируем случайный ключ для теста
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    # Это будет твоя ссылка на подключение. Потом она будет реальной.
    fake_link = f"vless://test-user-{random_string}@your-vps-ip:443?security=reality&sni=microsoft.com#VPN"
    return fake_link

# --- 3. ОБРАБОТЧИКИ БОТА ---

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Купить VPN (1 месяц)", callback_data="buy_vpn")]
    ])
    await message.answer(
        "🚀 Защищенный VPN-бот.\n\n"
        "Протокол: VLESS + Reality (скрытый от блокировок).\n"
        "Для покупки нажмите кнопку ниже.",
        reply_markup=keyboard
    )

@dp.callback_query(F.data == "buy_vpn")
async def buy_vpn(callback: types.CallbackQuery):
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title="VPN подписка 1 месяц",
        description="Доступ к скрытому серверу. Протокол Xray.",
        payload="vpn_month_1",
        provider_token="",
        currency="XTR",
        prices=[types.LabeledPrice(label="VPN на месяц (Xray)", amount=50)]
    )
    await callback.answer()

@dp.message(F.successful_payment)
async def payment_success(message: types.Message):
    user_id = message.from_user.id
    await message.answer("⏳ Оплата получена! Создаю твой скрытый конфиг...")

    try:
        # 1. Создаем пользователя на сервере (пока заглушка)
        config_link = create_vpn_user_on_server()
        
        # 2. Сохраняем в базу данных на 30 дней
        save_user_subscription(user_id, config_link)
        
        await message.answer(
            f"✅ Подписка активирована на 30 дней!\n\n"
            f"**Ссылка для подключения (V2Ray / Nekoray / Shadowrocket):**\n"
            f"`{config_link}`\n\n"
            f"🛡️ Протокол: VLESS + Reality. Трафик замаскирован.\n"
            f"📅 Подписка истекает через 30 дней. Для продления просто купите снова.",
            parse_mode="Markdown"
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка при создании VPN: {e}")

# --- 4. ЗАПУСК ---
async def main():
    init_db()  # Создаем БД при старте
    print("Бот с БД и готовностью к Xray запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
