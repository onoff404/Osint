import requests
from .utils import is_username

HEADERS = {"User-Agent": "Mozilla/5.0 (AllSee/1.0)"}
TIMEOUT = 12

def live_checks(query: str) -> dict:
    out: dict = {}
    q = query.strip()
    if is_username(q):
        u = q.lstrip("@")
        try:
            r = requests.get(f"https://api.github.com/users/{u}", headers=HEADERS, timeout=TIMEOUT)
            out["github"] = r.json() if r.status_code == 200 else {"http": r.status_code, "found": False}
        except Exception as ex:
            out["github"] = {"error": str(ex)}
    return out
