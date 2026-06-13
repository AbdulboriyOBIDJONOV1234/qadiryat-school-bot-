import re
from datetime import date, datetime


def is_valid_name_part(text: str) -> bool:
    text = text.strip()
    if not (2 <= len(text) <= 30):
        return False
    if " " in text:
        return False
    return all(ch.isalpha() or ch in "'’ʼʻ`-" for ch in text)


def parse_birth_date(text: str):
    text = text.strip()
    parsed = None
    for fmt in ("%d.%m.%Y", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            parsed = datetime.strptime(text, fmt).date()
            break
        except ValueError:
            continue

    if parsed is None:
        return None

    today = date.today()
    if parsed > today:
        return None

    age = today.year - parsed.year - ((today.month, today.day) < (parsed.month, parsed.day))
    if age < 3 or age > 100:
        return None

    return parsed


def parse_grade(text: str):
    digits = re.sub(r"\D", "", text)
    if not digits:
        return None

    grade = int(digits)
    if 1 <= grade <= 11:
        return grade
    return None


def is_valid_location(text: str) -> bool:
    text = text.strip()
    return 2 <= len(text) <= 150


def normalize_phone(text: str):
    digits = re.sub(r"\D", "", text)

    if len(digits) == 12 and digits.startswith("998"):
        return "+" + digits
    if len(digits) == 9:
        return "+998" + digits
    if len(digits) == 10 and digits[0] in ("0", "8"):
        return "+998" + digits[1:]

    return None
