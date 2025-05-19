import os
import telebot
import random
from dotenv import load_dotenv
from movie_data import movies_by_genre

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

user_language = {}

# Выбор языка
@bot.message_handler(commands=['start', 'hello'])
def choose_language(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Русский", "English")
    msg = bot.send_message(message.chat.id, "🌍 Выберите язык / Choose your language:", reply_markup=markup)
    bot.register_next_step_handler(msg, set_language)

def set_language(message):
    lang = message.text.strip().lower()
    user_id = message.from_user.id

    if lang == "русский":
        user_language[user_id] = "ru"
        bot.send_message(message.chat.id, "Привет! Напиши /movie, чтобы получить рекомендацию фильма. 🎬")
    elif lang == "english":
        user_language[user_id] = "en"
        bot.send_message(message.chat.id, "Hi! Type /movie to get a movie recommendation. 🎬")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, выберите Русский или English.")
        choose_language(message)

# Команда /movie
@bot.message_handler(commands=['movie'])
def ask_genre(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id)

    if not lang:
        choose_language(message)
        return

    genres = list(movies_by_genre[lang].keys())
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for genre in genres:
        markup.add(genre)

    text = "Выбери жанр:" if lang == "ru" else "Choose a genre:"
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, recommend_movie)

# Выдача фильма
def recommend_movie(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id)

    if not lang:
        choose_language(message)
        return

    genre = message.text.strip()
    if genre not in movies_by_genre[lang]:
        error_text = "❌ Такой жанр не найден. Попробуй ещё раз с /movie." if lang == "ru" else "❌ Genre not found. Try again with /movie."
        bot.send_message(message.chat.id, error_text)
        return

    movie = random.choice(movies_by_genre[lang][genre])
    reply = f"🎥 Рекомендую фильм из жанра *{genre}*:\n*{movie}*" if lang == "ru" else f"🎥 I recommend a *{genre}* movie:\n*{movie}*"
    bot.send_message(message.chat.id, reply, parse_mode="Markdown")

# Любое сообщение
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id)
    reply = "Напиши /movie чтобы получить фильм 🎬" if lang == "ru" else "Type /movie to get a movie 🎬"
    bot.send_message(message.chat.id, reply)

bot.infinity_polling()
