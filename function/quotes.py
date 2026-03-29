import random

STATHAM_QUOTES = [
    {
        "text": "Лучшая защита — это молча посмотреть в душу.",
        "image": "https://i.imgur.com/GjHMBKQ.jpeg"
    },
    {
        "text": "Мужчина должен быть сильным, молчаливым и умным. Как я.",
        "image": "https://i.imgur.com/WdRSM4v.jpeg"
    },
    {
        "text": "Я не говорю много. Но когда говорю — все молчат.",
        "image": "https://i.imgur.com/XBlTqKU.jpeg"
    },
    {
        "text": "Главное в жизни — это не бояться быть собой. Ну, или быть Стетхемом.",
        "image": "https://i.imgur.com/8rJjY3K.jpeg"
    },
    {
        "text": "Секрет успеха? Просто не сдавайся. И будь лысым.",
        "image": "https://i.imgur.com/LjW9o3M.jpeg"
    },
    {
        "text": "Когда жизнь даёт тебе лимоны — сожми кулаки и посмотри на неё.",
        "image": "https://i.imgur.com/QdRfG5h.jpeg"
    },
    {
        "text": "Настоящий мужчина не плачет. Он просто делает вид, что у него аллергия.",
        "image": "https://i.imgur.com/BqQX7YC.jpeg"
    },
    {
        "text": "Трудности закаляют характер. Особенно если ты Стетхем.",
        "image": "https://i.imgur.com/Uv7wQ8D.jpeg"
    },
    {
        "text": "Не бойся врагов. Бойся тех, кто молча смотрит тебе в глаза.",
        "image": "https://i.imgur.com/5tKqY2J.jpeg"
    },
    {
        "text": "Дисциплина — это когда ты делаешь то, что должен, даже если никто не смотрит.",
        "image": "https://i.imgur.com/RpMnK4F.jpeg"
    },
    {
        "text": "Я не агрессивен. Я просто целенаправленный.",
        "image": "https://i.imgur.com/6eVwN9G.jpeg"
    },
    {
        "text": "Жизнь коротка. Не трать её на то, что не имеет значения. Трать на спортзал.",
        "image": "https://i.imgur.com/2dKjT8Q.jpeg"
    },
    {
        "text": "Каждый день — это новая возможность стать лучше. Или хотя бы сильнее.",
        "image": "https://i.imgur.com/P4nRc7L.jpeg"
    },
    {
        "text": "Улыбка — это оружие. Особенно если ты лысый и серьёзный.",
        "image": "https://i.imgur.com/Vx3qY5H.jpeg"
    },
    {
        "text": "Не суди людей по их словам. Суди по тому, как они выглядят после боя.",
        "image": "https://i.imgur.com/J8mWk2D.jpeg"
    },
    {
        "text": "Раньше я думал, что сила — это мышцы. Потом понял, что сила — это молчание.",
        "image": "https://i.imgur.com/H9bNz4E.jpeg"
    },
    {
        "text": "Никогда не недооценивай человека, который молчит. Особенно если он лысый.",
        "image": "https://i.imgur.com/F7cPw6A.jpeg"
    },
    {
        "text": "Успех — это когда ты просыпаешься и понимаешь, что ты Стетхем.",
        "image": "https://i.imgur.com/K2dX8vR.jpeg"
    },
    {
        "text": "Если тебе кажется, что всё плохо — просто посмотри на мою голову. Она лысая и ей норм.",
        "image": "https://i.imgur.com/Z5nM9wT.jpeg"
    },
    {
        "text": "Самый сложный противник — это ты сам. Но я уже победил.",
        "image": "https://i.imgur.com/E4gR7yQ.jpeg"
    },
    {
        "text": "Не бойся перемен. Бойся оставаться таким же. Особенно слабым.",
        "image": "https://i.imgur.com/Q8kP3nW.jpeg"
    },
    {
        "text": "Мой стиль борьбы? Я просто прихожу и всё заканчивается.",
        "image": "https://i.imgur.com/W6jK5mX.jpeg"
    },
    {
        "text": "Сила — это не когда ты можешь всех побить. Сила — это когда ты не хочешь.",
        "image": "https://i.imgur.com/T9nB4zG.jpeg"
    },
    {
        "text": "Будь как вода. Или как Стетхем. Разницы нет.",
        "image": "https://i.imgur.com/L3kR6wD.jpeg"
    },
    {
        "text": "Если тебя не убило — ты стал сильнее. Если убило — ты был не Стетхем.",
        "image": "https://i.imgur.com/A7mQ8pJ.jpeg"
    },
    {
        "text": "Жизнь — это бой. Но я привык побеждать.",
        "image": "https://i.imgur.com/C2fN5vH.jpeg"
    },
    {
        "text": "Не ищи мотивацию. Будь мотивацией для других. Или хотя бы будь лысым.",
        "image": "https://i.imgur.com/S8dK4mF.jpeg"
    },
    {
        "text": "Когда тебе тяжело — помни: Стетхему тоже было тяжело. Но он был Стетхемом.",
        "image": "https://i.imgur.com/D6jR9wB.jpeg"
    },
    {
        "text": "Идеальный мужчина не существует. Но я близко.",
        "image": "https://i.imgur.com/M4kP7nG.jpeg"
    },
    {
        "text": "Не спорь с лысым. Он уже принял все решения.",
        "image": "https://i.imgur.com/Y1gN8tK.jpeg"
    },
]

RANDOM_REPLIES = [
    "Знаешь, что бы сказал Стетхем? Молча посмотрел бы на тебя.",
    "Это не тот вопрос, который задают Стетхему.",
    "Я бы ответил, но Стетхем отвечает кулаками.",
    "Ты серьёзно спрашиваешь у бота с цитатами Стетхема?",
    "Стетхем бы молча нажал /quote и посмотрел бы на тебя.",
    "Мне кажется, тебе нужна цитата. Нажми /quote.",
    "Хм. А что бы сказал Стетхем? Наверное, ничего. Он молчит.",
]


def get_random_quote() -> dict:
    return random.choice(STATHAM_QUOTES)


def get_random_reply() -> str:
    return random.choice(RANDOM_REPLIES)
