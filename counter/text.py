"""Counting rules for plain text. Language-agnostic; tested with Spanish and English."""

import re
import unicodedata
from dataclasses import asdict, dataclass

# A word is a run of letters/digits (any script, so á, ñ, ü work), optionally
# joined by an apostrophe or hyphen: "don't", "l'eau", "well-known".
# Numbers like 3.14 or 1,000 count as a single word.
_WORD = re.compile(r"\d+(?:[.,:]\d+)+|[^\W_]+(?:['’\-][^\W_]+)*")
_PARAGRAPH_BREAK = re.compile(r"\n\s*\n")


@dataclass(frozen=True)
class Counts:
    words: int
    characters: int
    characters_no_spaces: int
    paragraphs: int

    def to_dict(self) -> dict:
        return asdict(self)


def normalize(text: str) -> str:
    # NFC so "é" is one character whether it was typed or composed as e + ´.
    # Windows line endings would otherwise count as two characters.
    text = unicodedata.normalize("NFC", text)
    return text.replace("\r\n", "\n").replace("\r", "\n")


def count_text(text: str) -> Counts:
    text = normalize(text)
    return Counts(
        words=len(_WORD.findall(text)),
        characters=len(text),
        characters_no_spaces=sum(1 for c in text if not c.isspace()),
        paragraphs=sum(1 for p in _PARAGRAPH_BREAK.split(text) if p.strip()),
    )
