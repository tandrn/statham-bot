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
    caption = (
        f'\U0001f3ac "{quote["text"]}"\n'
        f"\u2014 \u0414\u0436\u0435\u0439\u0441\u043e\u043d \u0421\u0442\u0435\u0442\u0445\u0435\u043c"
    )
    await message.answer_photo(
        photo=quote["image"],
        caption=caption,
        reply_markup=build_quote_keyboard(),
    )


@router.message(Command("quote"))
async def cmd_quote(message: Message) -> None:
    quote = get_random_quote()
    caption = (
        f'\U0001f3ac "{quote["text"]}"\n'
        f"\u2014 \u0414\u0436\u0435\u0439\u0441\u043e\u043d \u0421\u0442\u0435\u0442\u0445\u0435\u043c"
    )
    await message.answer_photo(
        photo=quote["image"],
        caption=caption,
        reply_markup=build_quote_keyboard(),
    )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    text = (
        "\U0001f916 <b>\u0411\u043e\u0442 \u041c\u0435\u043c\u043d\u044b\u0445 \u0426\u0438\u0442\u0430\u0442 \u0421\u0442\u0435\u0442\u0445\u0435\u043c\u0430</b>\n\n"
        "\u041c\u0435\u043c\u043d\u044b\u0435 \u0446\u0438\u0442\u0430\u0442\u044b \u0434\u0436\u0435\u0439\u0441\u043e\u043d\u0430 \u0421\u0442\u0435\u0442\u0445\u0435\u043c\u0430 \u0441 \u0444\u043e\u0442\u043a\u0430\u043c\u0438! \U0001f4aa\n\n"
        "<b>\u041a\u043e\u043c\u0430\u043d\u0434\u044b:</b>\n"
        "/start \u2014 \u043f\u0440\u0438\u0432\u0435\u0442\u0441\u0442\u0432\u0438\u0435 + \u0446\u0438\u0442\u0430\u0442\u0430\n"
        "/quote \u2014 \u0440\u0430\u043d\u0434\u043e\u043c\u043d\u0430\u044f \u0446\u0438\u0442\u0430\u0442\u0430\n"
        "/help \u2014 \u044d\u0442\u0430 \u0441\u043f\u0440\u0430\u0432\u043a\u0430\n\n"
        "\u041d\u0430\u043f\u0438\u0448\u0438 \u043b\u044e\u0431\u043e\u0439 \u0442\u0435\u043a\u0441\u0442 \u2014 \u043f\u043e\u043b\u0443\u0447\u0438\u0448\u044c \u043c\u0435\u043c\u043d\u044b\u0439 \u043e\u0442\u0432\u0435\u0442."
    )
    await message.answer(text, parse_mode="HTML")


@router.callback_query(F.data == "another_quote")
async def callback_another_quote(callback: CallbackQuery) -> None:
    quote = get_random_quote()
    caption = (
        f'\U0001f3ac "{quote["text"]}"\n'
        f"\u2014 \u0414\u0436\u0435\u0439\u0441\u043e\u043d \u0421\u0442\u0435\u0442\u0445\u0435\u043c"
    )
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
        caption = (
            f'\U0001f3ac "{q["text"]}"\n'
            f"\u2014 \u0414\u0436\u0435\u0439\u0441\u043e\u043d \u0421\u0442\u0435\u0442\u0445\u0435\u043c"
        )
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
