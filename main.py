import asyncio
import json

from aiogram import types
from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiohttp import web
from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

bot = Bot(token='7028494517:AAEiIPjbRdn7EY-IupFwIF9pEBegJaUogDI')
dp = Dispatcher()

USERS_FILE = 'users.json'
TOP_HTML_FILE = 'top.html'

def load_users():
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as file:
            # Загружаем список пользователей из файла JSON
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Если файл не найден или возникает ошибка декодирования JSON,
        # возвращаем пустой список пользователей
        return []

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as file:
        json.dump(users, file, ensure_ascii=False, indent=4)

def update_top_html(users):
    sorted_users = sorted(users, key=lambda x: x['balance'], reverse=True)[:10]
    with open(TOP_HTML_FILE, 'w', encoding='utf-8') as file:
        file.write('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n')
        file.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        file.write('<title>Top Players</title>\n</head>\n<body>\n<h1>Топ Игроков</h1>\n<ol>\n')
        for user in sorted_users:
            file.write(f'<li>{user["username"]}: Баланс {user["balance"]}, Население {user["population"]}</li>\n')
        file.write('</ol>\n</body>\n</html>')

async def save_user_info(user_id: int, username: str, first_name: str, league: str, balance: int, population: int):
    users = load_users()
    user_info = {
        "user_id": user_id,
        "username": username,
        "first_name": first_name,
        "league": league,
        "balance": balance,
        "population": population
    }

    # Проверяем, существует ли пользователь в базе данных
    existing_user = next((user for user in users if user['user_id'] == user_id), None)
    if existing_user:
        # Если пользователь уже существует, просто обновляем его информацию
        existing_user.update(user_info)
    else:
        # Если пользователь новый, выдаем ему стартовый пакет
        user_info['balance'] = 100
        user_info['population'] = 50
        users.append(user_info)

    save_users(users)
    update_top_html(users)

@dp.message(Command('start'))
async def start(message: types.Message):
    # Пример значений, которые можно получить или хранить
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"
    first_name = message.from_user.first_name or "Unknown"
    league = "Начинающий"  # Вам нужно определить лигу игрока
    balance = 0  # Вам нужно определить баланс игрока
    population = 0  # Вам нужно определить население игрока

    await save_user_info(user_id, username, first_name, league, balance, population)

    item1 = KeyboardButton(text="Open", web_app=WebAppInfo(url='https://derzkiu1.github.io/discrit/'))
    keyboard = ReplyKeyboardMarkup(keyboard=[[item1]], resize_keyboard=True)
    await bot.send_message(message.from_user.id, 'Welcome', reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

