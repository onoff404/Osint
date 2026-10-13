import re

def clean(s: str) -> str:
    return s.strip()

def digits_of(s: str) -> str:
    return re.sub(r"\D", "", s)

def is_phone(q: str) -> bool:
    d = digits_of(q)
    return 7 <= len(d) <= 15 and len(d) >= len(q.strip()) * 0.5

def is_email(q: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", q.strip()))

def is_username(q: str) -> bool:
    q = q.strip()
    return bool(re.match(r"^@?[A-Za-z0-9_.\-]{2,30}$", q)) and " " not in q

def classify(q: str) -> str:
    if is_email(q):
        return "email"
    if is_phone(q):
        return "phone"
    if is_username(q):
        return "username"
    return "name"
