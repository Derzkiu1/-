import sqlite3
import telebot
from telebot import types
import os

TOKEN = '7492402331:AAFv8J8fShA8kz-ZauRHVcQDb8KFr8s51wY'  # Замените на ваш реальный токен
WEB_APP_URL = 'https://derzkiu1.github.io/-/'  # Замените на URL вашего веб-приложения

bot = telebot.TeleBot(TOKEN)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            username TEXT,
            coins INTEGER DEFAULT 0
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS referrals (
            user_id INTEGER,
            referral_telegram_id INTEGER,
            referral_username TEXT,
            coins_earned INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(telegram_id)
        )
    ''')
    conn.commit()
    conn.close()

def add_user(telegram_id, username):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO users (telegram_id, username) VALUES (?, ?)', (telegram_id, username))
    conn.commit()
    conn.close()

def add_referral(user_id, referral_telegram_id, referral_username, coins_earned):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO referrals (user_id, referral_telegram_id, referral_username, coins_earned)
        VALUES (?, ?, ?, ?)
    ''', (user_id, referral_telegram_id, referral_username, coins_earned))
    conn.commit()
    conn.close()

def get_user_data(telegram_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
    user_data = c.fetchone()
    conn.close()
    return user_data

def get_referrals_data(user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM referrals WHERE user_id = ?', (user_id,))
    referrals_data = c.fetchall()
    conn.close()
    return referrals_data

def generate_html(telegram_id):
    user_data = get_user_data(telegram_id)
    referrals_data = get_referrals_data(telegram_id)

    if user_data and referrals_data:
        username, coins = user_data[1], user_data[2]
        referral_list_items = ''.join(
            f'<li><i class="fas fa-user-plus"></i><span>{referral[2]}</span><span>{referral[3]} coins</span></li>'
            for referral in referrals_data
        )

        with open('template.html', 'r') as template_file:
            template_content = template_file.read()
            html_content = template_content.format(
                username=username,
                coins=coins,
                referral_list_items=referral_list_items,
                telegram_id=telegram_id
            )

        with open(f'{telegram_id}.html', 'w') as file:
            file.write(html_content)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    telegram_id = message.from_user.id
    username = message.from_user.username
    add_user(telegram_id, username)
    generate_html(telegram_id)

    # Создаем кнопку Web App
    web_app_button = types.WebAppInfo(WEB_APP_URL)
    markup = types.ReplyKeyboardMarkup(row_width=1)
    web_app_markup = types.KeyboardButton(text="Open Web App", web_app=web_app_button)
    markup.add(web_app_markup)

    bot.send_message(message.chat.id, f"Welcome {username}! Click the button below to open the web app.", reply_markup=markup)

if __name__ == '__main__':
    print("Initializing database...")
    init_db()
    print("Starting bot...")
    bot.polling()
