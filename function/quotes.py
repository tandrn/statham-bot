import json
import random
from pathlib import Path

QUOTES_PATH = Path(__file__).parent / "quotes.json"

_quotes: list[dict] = []


def _load_quotes() -> list[dict]:
    global _quotes
    if not _quotes:
        with open(QUOTES_PATH, "r", encoding="utf-8") as f:
            _quotes = json.load(f)
    return _quotes


def get_random_quote() -> str:
    quotes = _load_quotes()
    return random.choice(quotes)["text"]


def get_all_quotes() -> list[str]:
    quotes = _load_quotes()
    return [q["text"] for q in quotes]
