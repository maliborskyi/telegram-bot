import telebot
from telebot import types
import datetime

TOKEN = '8939916500:AAHiG9ijuFzu4oWKlMSqdo_651Pwi3VQxKA'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_help = types.InlineKeyboardButton("📜 Допомога", callback_data="help_info")
    btn_site = types.InlineKeyboardButton("🌐 Мій GitHub", url="https://github.com/")
    markup.add(btn_help, btn_site)
    
    bot.reply_to(
        message, 
        f"Привіт, {message.from_user.first_name}! 👋\n"
        "Даний бот успішно працює на хмарному сервері AWS! 🚀\n"
        "Використай команду /help, щоб переглянути список доступних можливостей.",
        reply_markup=markup
    )

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "📜 **Доступні команди бота:**\n\n"
        "/start — Запустити бота привітанням\n"
        "/help — Показати це меню допомоги\n"
        "/time — Дізнатися поточний час на сервері\n"
        "/calc — Простий калькулятор (приклад: `/calc 10 + 5`)\n\n"
        "Також я просто повторюю будь-яке твоє текстове повідомлення (ехо-режим)!"
    )
    bot.reply_to(message, help_text, parse_mode="Markdown")

@bot.message_handler(commands=['time'])
def send_time(message):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bot.reply_to(message, f"⏰ Поточний час на сервері AWS: `{current_time}`", parse_mode="Markdown")

@bot.message_handler(commands=['calc'])
def calculate(message):
    try:
        parts = message.text.split()
        if len(parts) != 4:
            bot.reply_to(message, "⚠️ Неправильний формат! Використовуй так: `/calc 10 + 5`", parse_mode="Markdown")
            return
        
        num1 = float(parts[1])
        op = parts[2]
        num2 = float(parts[3])
        
        if op == '+':
            res = num1 + num2
        elif op == '-':
            res = num1 - num2
        elif op == '*':
            res = num1 * num2
        elif op == '/':
            if num2 == 0:
                bot.reply_to(message, "❌ На нуль ділити не можна!")
                return
            res = num1 / num2
        else:
            bot.reply_to(message, "⚠️ Невідома операція! Використовуй +, -, *, /")
            return
            
        bot.reply_to(message, f"🧮 Результат: `{num1} {op} {num2} = {res}`", parse_mode="Markdown")
    except ValueError:
        bot.reply_to(message, "⚠️ Помилка! Вводь числа, а не букви.")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "help_info":
        bot.answer_callback_query(call.id, "Ви натиснули кнопку допомоги!")
        bot.send_message(call.message.chat.id, "💡 Нагадую, що всі команди можна подивитися через /help.")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, f"💬 Ти написав: «{message.text}». Я просто бот, але чудово тебе розумію! 😊")

if __name__ == '__main__':
    print("Бот запущено і він чекає на повідомлення...")
    bot.infinity_polling()