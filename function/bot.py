import os
import io
import logging
import aiohttp
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    BufferedInputFile,
)
from quotes import get_random_quote
from meme_generator import generate_meme, get_random_template_url

logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

WISDOM_MODE: dict[int, bool] = {}


def build_main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="\U0001f4a1 Мудрость дня",
                    callback_data="wisdom",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="\U0001f525 Ещё цитату!",
                    callback_data="another_quote",
                ),
                InlineKeyboardButton(
                    text="\U0001f4dd Свой текст",
                    callback_data="custom_text",
                ),
            ],
        ]
    )


def build_after_custom_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="\U0001f4a1 Мудрость дня",
                    callback_data="wisdom",
                ),
                InlineKeyboardButton(
                    text="\U0001f525 Ещё цитату!",
                    callback_data="another_quote",
                ),
            ],
        ]
    )


async def _download_image(url: str) -> bytes:
    headers = {"User-Agent": "StathamBot/1.0 (Telegram bot; +https://t.me/statham_foreva_bot)"}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            data = await resp.read()
            logger.info("Downloaded %s: %d bytes, status=%d, content-type=%s", url[:60], len(data), resp.status, resp.content_type)
            return data


async def _send_meme(message_or_callback, quote: str, reply_markup=None) -> None:
    template_url = get_random_template_url()
    try:
        image_bytes = await _download_image(template_url)
        meme_bytes = generate_meme(image_bytes, quote)
        photo = BufferedInputFile(meme_bytes, filename="meme.jpg")
    except Exception as e:
        logger.error("Meme generation failed: %s", e)
        photo = template_url

    caption = f'\U0001f9e0 \u00ab{quote}\u00bb'

    if isinstance(message_or_callback, CallbackQuery):
        msg = message_or_callback.message
        if isinstance(photo, BufferedInputFile):
            await msg.answer_photo(
                photo=photo,
                caption=caption,
                reply_markup=reply_markup or build_main_keyboard(),
            )
        else:
            await msg.answer_photo(
                photo=photo,
                caption=caption,
                reply_markup=reply_markup or build_main_keyboard(),
            )
    else:
        await message_or_callback.answer_photo(
            photo=photo,
            caption=caption,
            reply_markup=reply_markup or build_main_keyboard(),
        )


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    text = (
        "\U0001f3ac <b>Мемный Бот Стетхема</b>\n\n"
        "120 мемных цитат + генератор мемов!\n\n"
        "\U0001f4a1 <b>Мудрость дня</b> — рандомная цитата с серьёзным лицом\n"
        "\U0001f525 <b>Ещё цитату!</b> — следующая мемная цитата\n"
        "\U0001f4dd <b>Свой текст</b> — напиши свой текст, я наложу на фото!\n\n"
        "Команды: /quote /custom /help"
    )
    await message.answer(text, parse_mode="HTML")
    quote = get_random_quote()
    await _send_meme(message, quote)


@router.message(Command("quote"))
async def cmd_quote(message: Message) -> None:
    quote = get_random_quote()
    await _send_meme(message, quote)


@router.message(Command("custom"))
async def cmd_custom(message: Message) -> None:
    WISDOM_MODE[message.from_user.id] = True
    await message.answer(
        "\U0001f4dd Напиши свой текст — я наложу его на фото Стетхема!"
    )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    text = (
        "\U0001f916 <b>Мемный Бот Стетхема</b>\n\n"
        "\U0001f3ac 120 мемных цитат Стетхема с генератором мемов!\n\n"
        "<b>Команды:</b>\n"
        "/start \u2014 приветствие + цитата\n"
        "/quote \u2014 рандомная мемная цитата\n"
        "/custom \u2014 написать свой текст\n"
        "/help \u2014 эта справка\n\n"
        "<b>Кнопки:</b>\n"
        "\U0001f4a1 Мудрость дня \u2014 цитата с серьёзным лицом\n"
        "\U0001f525 Ещё цитату! \u2014 следующая цитата\n"
        "\U0001f4dd Свой текст \u2014 ввести свой текст для мема"
    )
    await message.answer(text, parse_mode="HTML")


@router.callback_query(F.data == "another_quote")
async def callback_another_quote(callback: CallbackQuery) -> None:
    quote = get_random_quote()
    await _send_meme(callback, quote)
    await callback.answer()


@router.callback_query(F.data == "wisdom")
async def callback_wisdom(callback: CallbackQuery) -> None:
    quote = get_random_quote()
    wisdom_text = f'\U0001f4a1 Мудрость дня:\n\n\u00ab{quote}\u00bb\n\n\u2014 Джейсон Стетхем'
    template_url = get_random_template_url()
    try:
        image_bytes = await _download_image(template_url)
        meme_bytes = generate_meme(image_bytes, quote)
        photo = BufferedInputFile(meme_bytes, filename="wisdom.jpg")
    except Exception as e:
        logger.error("Wisdom meme failed: %s", e)
        photo = template_url

    await callback.message.answer_photo(
        photo=photo,
        caption=wisdom_text,
        reply_markup=build_main_keyboard(),
    )
    await callback.answer("\U0001f4a1 Мудрость получена!")


@router.callback_query(F.data == "custom_text")
async def callback_custom_text(callback: CallbackQuery) -> None:
    WISDOM_MODE[callback.from_user.id] = True
    await callback.message.answer(
        "\U0001f4dd Напиши свой текст — я наложу его на фото Стетхема!"
    )
    await callback.answer()


@router.message()
async def any_message(message: Message) -> None:
    user_id = message.from_user.id

    if WISDOM_MODE.get(user_id):
        WISDOM_MODE[user_id] = False
        custom_text = message.text.strip()
        if not custom_text:
            await message.answer("\U0001f6ab Текст пустой, попробуй ещё раз!")
            return

        template_url = get_random_template_url()
        try:
            image_bytes = await _download_image(template_url)
            meme_bytes = generate_meme(image_bytes, custom_text)
            photo = BufferedInputFile(meme_bytes, filename="custom_meme.jpg")
        except Exception as e:
            logger.error("Custom meme failed: %s", e)
            photo = template_url

        await message.answer_photo(
            photo=photo,
            caption=f'\U0001f3ac Твой мем:\n\n\u00ab{custom_text}\u00bb',
            reply_markup=build_after_custom_keyboard(),
        )
        return

    quote = get_random_quote()
    await message.answer(
        f'\U0001f9e0 \u00ab{quote}\u00bb\n\nНажми /quote для новой цитаты!'
    )


dp.include_router(router)
