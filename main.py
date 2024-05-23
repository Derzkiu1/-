import asyncio
import json

from aiogram import types
from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiohttp import web
from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo,InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token='7028494517:AAEiIPjbRdn7EY-IupFwIF9pEBegJaUogDI')
dp = Dispatcher()

USERS_FILE = 'users.json'

def load_users():
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as file:
        json.dump(users, file, ensure_ascii=False, indent=4)

async def save_user_info(user_id: int, username: str, first_name: str, league: str, balance: int, population: int):
    users = load_users()
    user_info = {
        "user_id": user_id,
        "username": username,
        "first_name": first_name,
        "league": league,
        "balance": balance,
        "population": population,
        "totalProfit": 0,
        "items": [
            {
                "name": "Помощь бедным",
                "price": 100,
                "priceIncrement": 25,
                "profit": 25,
                "profitIncrement": 2.5,
                "population": 10,
                "populationIncrement": 1,
                "level": 0
            }
        ]
    }

    existing_user = next((user for user in users if user['user_id'] == user_id), None)
    if existing_user:
        # Обновляем информацию о существующем пользователе, сохраняя уровни товаров
        existing_user.update({
            "username": username,
            "first_name": first_name,
            "league": league,
            "balance": balance,
            "population": population
        })
    else:
        # Новый пользователь получает начальные значения
        user_info['balance'] = 500
        user_info['population'] = 150
        users.append(user_info)

    save_users(users)

@dp.message(Command('start'))
async def start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"
    first_name = message.from_user.first_name or "Unknown"
    league = "Начинающий"
    balance = 0
    population = 0

    await save_user_info(user_id, username, first_name, league, balance, population)

    # Создаем инлайн-кнопку с WebAppInfo
    web_app_button = InlineKeyboardButton(
        text="Open",
        web_app=WebAppInfo(url='https://derzkiu1.github.io/-/')
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[web_app_button]])

    await bot.send_message(message.from_user.id, 'Welcome', reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
