# 🎬 Мемные Цитаты Стетхема — Telegram Bot

Telegram-бот, который отправляет мемные цитаты Джейсона Стетхема с фотографиями. Разворачивается на Yandex Cloud Functions.

## Функционал

- `/start` — приветствие + первая цитата
- `/quote` — рандомная цитата Стетхема с фото
- `/help` — справка
- Кнопка «🔥 Ещё цитату!» — следующая цитата
- Кнопка «🔗 Поделиться» — inline-режим для пересылки
- Любой текст → мемный ответ в духе Стетхема

## Стек

- Python 3.12
- aiogram 3.x
- Yandex Cloud Functions (serverless)

## Структура

```
statham-bot/
├── function/
│   ├── index.py          # Cloud Function entry point (webhook)
│   ├── bot.py            # Handlers бота, inline-кнопки
│   ├── quotes.py         # Коллекция мемных цитат (~30 шт.)
│   └── requirements.txt  # Зависимости
├── deploy.sh             # Скрипт деплоя (bash)
└── README.md
```

## Установка и деплой

### 1. Предварительные требования

- Установленный [Yandex Cloud CLI](https://yandex.cloud/ru/docs/cli/quickstart)
- Аутентификация в YC: `yc init`
- Аккаунт Telegram и [@BotFather](https://t.me/BotFather)

### 2. Создай бота

1. Открой [@BotFather](https://t.me/BotFather)
2. Отправь `/newbot`
3. Следуй инструкциям, получишь **токен** вида `123456:ABC-DEF...`

### 3. Настрой скрипт деплоя

Открой `deploy.sh` и замени:

```bash
BOT_TOKEN="ВСТАВЬ_СВОЙ_ТОКЕН_СЮДА"
```

### 4. Запусти деплой

```bash
chmod +x deploy.sh
./deploy.sh
```

Скрипт автоматически:
- Создаст Cloud Function
- Зальёт код
- Установит Telegram webhook

### 5. Тестируй

Открой Telegram → найди своего бота → нажми `/start` 🎉

## Локальная разработка (polling)

```bash
cd function
pip install -r requirements.txt
```

Создай файл `local.py`:

```python
import asyncio
from bot import bot, dp

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
```

Запусти:

```bash
BOT_TOKEN="твой_токен" python local.py
```

## Стоимость

| Сервис | Стоимость |
|--------|-----------|
| Yandex Cloud Functions | Бесплатно (до 1 млн вызовов/мес) |
| Telegram Bot API | Бесплатно |
| Хостинг фоток (Imgur) | Бесплатно |

## Лицензия

MIT
