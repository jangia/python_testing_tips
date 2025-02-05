import re


def is_valid_email(email: str) -> bool:
    return bool(re.search(r"^[\w\.\-\+']+@[\w\.\-]+\.\w+$", email))