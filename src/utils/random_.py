import random
from string import ascii_lowercase


def rand_int(start: int, end: int) -> int:
    return random.randrange(start, end)


def rand_word(words: set) -> str:
    return random.choice(list(words))


def rand_letter() -> str:
    return random.choice(list(ascii_lowercase))


def rand_hex():
    return "%02x" % random.randint(0, 255)


def rand_color():
    return f"{rand_hex()}{rand_hex()}{rand_hex()}"
