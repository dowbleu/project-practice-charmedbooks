# Создание Telegram-бота для рекомендаций фильмов на Python

## Исследование предметной области

### Обзор

В этом проекте реализован Telegram-бот MovieBot, который:

1. Общается с пользователем на русском или английском языке.
2. Принимает команды и предлагает жанры фильмов.
3. Отправляет случайную рекомендацию фильма по выбранному жанру.

Проект показывает, как можно создать простого, но полезного чат-бота с использованием Python и Telegram Bot API. Основной упор сделан на простоту архитектуры, локальную базу данных фильмов и минимальные зависимости.

## Техническое руководство

### Поддерживаемый функционал MovieBot

Бот поддерживает следующие команды и функции:

- `/start` — выбор языка взаимодействия.
- `/movie` — отображение списка жанров и рекомендация фильма.
- Поддержка русского и английского языков.
- Отправка сообщений и взаимодействие с кнопками в Telegram.

### Этап 1: Получение токена и настройка окружения

Чтобы запустить своего Telegram-бота, выполните следующие шаги:

1. Откройте Telegram и найдите бота `@BotFather`.
2. Отправьте команду `/start`, затем — `/newbot`.
3. Задайте имя и уникальный username (должен оканчиваться на `bot`).
4. Скопируйте токен API, который выдаст BotFather.
5. Перейдите в файл [.env](../src/.env) и вставьте туда ваш токен

### Этап 2: Получение токена и настройка окружения

Проект состоит из двух файлов:

- `bot.py` — основной обработчик логики Telegram-бота.
- `movie_data.py` — локальная база данных фильмов по жанрам на русском и английском.

Также используется файл `.env` для хранения секретного токена.

### Этап 3: Запуск бота

1. Клонируйте или скачайте репозиторий с файлами `bot.py`, `movie_data.py`, `.env`.
2. Убедитесь, что токен прописан в `.env`.
3. В терминале перейдите в папку с ботом и запустите командой `python bot.py`

Если всё сделано правильно, бот будет готов к приёму команд.

### Этап 4: Использование

1. Откройте Telegram и найдите своего бота по username.
2. Введите `/start`, выберите язык общения.
3. Введите `/movie`, выберите жанр.
4. Получите персональную рекомендацию фильма!

### Пример ключевых фрагментов кода:

- Загрузка токена из `.env`:

```python
import telebot

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Выберите язык: Русский или English")
```

- Инициализация бота и обработка команды `/start`:

```python
import telebot

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Выберите язык: Русский или English")

```

- Обработка команды `/movie` и выбор жанра:

```python
@bot.message_handler(commands=['movie'])
def send_genres(message):
    genres = ["Комедия", "Драма", "Фантастика", "Ужасы"]
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for genre in genres:
        markup.add(genre)
    bot.send_message(message.chat.id, "Выберите жанр фильма:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["Комедия", "Драма", "Фантастика", "Ужасы"])
def send_movie_recommendation(message):
    genre = message.text
    movie = get_movie_recommendation(genre)  # Функция из movie_data.py
    bot.send_message(message.chat.id, f"Рекомендуемый фильм: {movie}")
```

---
[Видео-демонстрация работы движка](./variative_presentation.mov)