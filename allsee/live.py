import hashlib
import requests
from .utils import is_username, is_email

HEADERS = {"User-Agent": "Mozilla/5.0 (AllSee/1.0)"}
TIMEOUT = 10

SITES = [
    ("github", "https://github.com/{u}"),
    ("gitlab", "https://gitlab.com/{u}"),
    ("reddit", "https://www.reddit.com/user/{u}/"),
    ("medium", "https://medium.com/@{u}"),
    ("devto", "https://dev.to/{u}"),
    ("kaggle", "https://www.kaggle.com/{u}"),
    ("npm", "https://www.npmjs.com/~{u}"),
    ("pypi", "https://pypi.org/user/{u}/"),
    ("x", "https://x.com/{u}"),
    ("instagram", "https://instagram.com/{u}"),
    ("tiktok", "https://tiktok.com/@{u}"),
]

def _get(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        return r.status_code, r.text[:2000]
    except Exception as ex:
        return -1, str(ex)

def live_checks(query: str) -> dict:
    out: dict = {}
    q = query.strip()
    if is_username(q):
        u = q.lstrip("@")
        res = {}
        for name, tpl in SITES:
            url = tpl.format(u=u)
            code, _ = _get(url)
            # 200 = exists (heuristic), 404 = free, -1 = blocked/error
            if code == 200:
                res[name] = {"found": True, "url": url}
            elif code == 404:
                res[name] = {"found": False}
            else:
                res[name] = {"http": code, "url": url, "unsure": True}
        try:
            r = requests.get(f"https://api.github.com/users/{u}", headers=HEADERS, timeout=TIMEOUT)
            res["github_api"] = r.json() if r.status_code == 200 else {"found": False}
        except Exception as ex:
            res["github_api"] = {"error": str(ex)}
        out["usernames"] = res
    if is_email(q):
        h = hashlib.md5(q.strip().lower().encode()).hexdigest()
        code, _ = _get(f"https://www.gravatar.com/avatar/{h}?d=404")
        out["gravatar"] = {"hash": h, "has_avatar": code == 200,
                           "url": f"https://www.gravatar.com/avatar/{h}"}
    return out
