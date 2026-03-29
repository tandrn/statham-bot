import json
import asyncio
import logging
from bot import bot, dp

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
    except (json.JSONDecodeError, TypeError):
        return {"statusCode": 400, "body": "invalid json"}

    logger.info("Received update: %s", body)

    from aiogram.types import Update

    update = Update.model_validate(body)

    asyncio.get_event_loop().run_until_complete(
        dp.feed_update(bot, update)
    )

    return {"statusCode": 200, "body": "ok"}
