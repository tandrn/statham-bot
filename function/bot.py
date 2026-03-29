import os
import logging
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQuery,
    InlineQueryResultCachedPhoto,
    InputTextMessageContent,
)
from quotes import get_random_quote, get_random_reply

logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()


def build_quote_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="\U0001f525 Ещё цитату!",
                    callback_data="another_quote",
                ),
                InlineKeyboardButton(
                    text="\U0001f517 Поделиться",
                    switch_inline_query="quote",
                ),
            ],
        ]
    )


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    quote = get_random_quote()
    caption = f'\U0001f9e0 "{quote["text"]}"'
    await message.answer_photo(
        photo=quote["image"],
        caption=caption,
        reply_markup=build_quote_keyboard(),
    )


@router.message(Command("quote"))
async def cmd_quote(message: Message) -> None:
    quote = get_random_quote()
    caption = f'\U0001f9e0 "{quote["text"]}"'
    await message.answer_photo(
        photo=quote["image"],
        caption=caption,
        reply_markup=build_quote_keyboard(),
    )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    text = (
        "\U0001f916 <b>Бот Мемных Тикток Цитат</b>\n\n"
        "Рандомные мемные цитаты с картинками! \U0001f4aa\n\n"
        "<b>Команды:</b>\n"
        "/start \u2014 приветствие + цитата\n"
        "/quote \u2014 рандомная цитата\n"
        "/help \u2014 эта справка\n\n"
        "Напиши любой текст \u2014 получишь мемный ответ."
    )
    await message.answer(text, parse_mode="HTML")


@router.callback_query(F.data == "another_quote")
async def callback_another_quote(callback: CallbackQuery) -> None:
    quote = get_random_quote()
    caption = f'\U0001f9e0 "{quote["text"]}"'
    await callback.message.edit_media(
        media={
            "type": "photo",
            "media": quote["image"],
            "caption": caption,
            "parse_mode": "HTML",
        },
        reply_markup=build_quote_keyboard(),
    )
    await callback.answer()


@router.inline_query(F.query == "quote")
async def inline_query_quote(inline_query: InlineQuery) -> None:
    results = []
    for i in range(10):
        q = get_random_quote()
        caption = f'\U0001f9e0 "{q["text"]}"'
        results.append(
            InlineQueryResultCachedPhoto(
                id=str(i),
                photo_file_id=q.get("file_id", ""),
                caption=caption,
            )
        )
    await inline_query.answer(results, cache_time=30)


@router.message()
async def any_message(message: Message) -> None:
    reply = get_random_reply()
    await message.answer(reply)


dp.include_router(router)
