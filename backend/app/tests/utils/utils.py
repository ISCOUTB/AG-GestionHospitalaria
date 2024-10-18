import random
import string


def random_document() -> str:
    list_numbers: list[int] = random.choices(range(0, 10), k=10)
    return "".join(str(x) for x in list_numbers)


def random_password(k: int) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=k))
