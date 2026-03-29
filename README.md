<div align="center">

# Мемные Цитаты Стетхема

**Telegram-бот с мемными цитатами Джейсона Стетхема и его фотками**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-26A5E4?logo=telegram&logoColor=white)](https://docs.aiogram.dev/)
[![Yandex Cloud](https://img.shields.io/badge/Yandex_Cloud-Functions-FCC734?logo=yandexcloud&logoColor=black)](https://yandex.cloud/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

<img src="https://media.giphy.com/media/3o7TKwmnDgQb5jemjK/giphy.gif" width="200" alt="Statham">

</div>

## Что умеет бот

| Команда / Действие | Описание |
|:---|:---|
| `/start` | Приветствие + первая цитата с фото |
| `/quote` | Рандомная мемная цитата Стетхема + фото |
| `/help` | Справка по командам |
| Кнопка **«Ещё цитату!»** | Следующая цитата (inline) |
| Кнопка **«Поделиться»** | Inline-режим для пересылки друзьям |
| Любой текст | Мемный ответ в духе Стетхема |

## Скриншоты

<div align="center">

| Старт | Цитата |
|:---:|:---:|
| <img src="https://i.imgur.com/GjHMBKQ.jpeg" width="250"> | <img src="https://i.imgur.com/WdRSM4v.jpeg" width="250"> |

</div>

## Стек

- **Python 3.12** — язык
- **aiogram 3.x** — Telegram Bot API фреймворк
- **Yandex Cloud Functions** — серверлесс-деплой
- **30 мемных цитат** с фотками Стетхема

## Структура проекта

```
statham-bot/
├── function/
│   ├── index.py          # Cloud Function entry point (webhook)
│   ├── bot.py            # Handlers бота, inline-кнопки
│   ├── quotes.py         # Коллекция мемных цитат (~30 шт.)
│   ├── local.py          # Локальный запуск (polling)
│   └── requirements.txt  # Зависимости
├── deploy.sh             # Скрипт деплоя
├── .gitignore
└── README.md
```

## Быстрый старт

### 1. Клонируй репозиторий

```bash
git clone https://github.com/tandrn/statham-bot.git
cd statham-bot
```

### 2. Создай бота

1. Открой [@BotFather](https://t.me/BotFather) в Telegram
2. Отправь `/newbot`
3. Следуй инструкциям и получи **токен**

### 3. Локальный запуск (polling)

```bash
cd function
pip install -r requirements.txt
set BOT_TOKEN=your_token_here
python local.py
```

### 4. Деплой на Yandex Cloud Functions

#### Через консоль (рекомендуется)

1. Зайди на [console.yandex.cloud](https://console.yandex.cloud)
2. Найди **Cloud Functions** (через поиск)
3. Создай функцию `statham-bot`
4. Загрузи файлы из папки `function/` в редактор
5. Настрой:
   - **Точка входа**: `index.handler`
   - **Runtime**: Python 3.12
   - **Таймаут**: 30 секунд
   - **Переменные окружения**: `BOT_TOKEN` = `your_token`
6. Создай триггер **HTTP** (без авторизации)
7. Установи webhook:
   ```
   https://api.telegram.org/bot<TOKEN>/setWebhook?url=<FUNCTION_URL>
   ```

#### Через CLI (автоматически)

```bash
# Установи Yandex Cloud CLI: https://yandex.cloud/ru/docs/cli/quickstart
chmod +x deploy.sh

# Открой deploy.sh и замени BOT_TOKEN
./deploy.sh
```

## Переменные окружения

| Переменная | Описание | Обязательная |
|:---|:---|:---:|
| `BOT_TOKEN` | Токен бота от @BotFather | Да |

## Стоимость

| Сервис | Стоимость |
|:---|:---|
| Yandex Cloud Functions | **Бесплатно** (до 1 млн вызовов/мес) |
| Telegram Bot API | **Бесплатно** |
| Хостинг фоток (Imgur) | **Бесплатно** |

> Бот полностью бесплатный в эксплуатации!

## Roadmap

- [ ] Добавить больше цитат и фоток
- [ ] Inline-режим с выбором категории цитат
- [ ] Статистика использования бота
- [ ] Мультиязычность (EN / RU)
- [ ] Случайные фото через Unsplash API
- [ ] Голосовые сообщения с цитатами

## FAQ

**Q: Бот не отвечает после деплоя?**
A: Проверь, что webhook установлен: `https://api.telegram.org/bot<TOKEN>/getWebhookInfo`

**Q: Как добавить свои цитаты?**
A: Открой `function/quotes.py` и добавь в список `STATHAM_QUOTES`.

**Q: Бесплатно ли это?**
A: Да! Yandex Cloud Functions бесплатен до 1 млн вызовов в месяц.

## Контакты

**Даниэл Жанышов** — Python Developer

- GitHub: [@tandrn](https://github.com/tandrn)

## Лицензия

MIT License — см. [LICENSE](LICENSE) для деталей.

---

<div align="center">

**Если тебе понравился бот — поставь звёздочку!**

[![Star](https://img.shields.io/github/stars/tandrn/statham-bot?style=social)](https://github.com/tandrn/statham-bot)

</div>
