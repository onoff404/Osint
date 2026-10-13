import urllib.parse
from dataclasses import dataclass
from .utils import clean, digits_of, is_phone, is_email, is_username

@dataclass
class Hit:
    source: str
    url: str
    note: str = ""

def enc(q: str) -> str:
    return urllib.parse.quote_plus(q)

def build_targets(query: str) -> list[Hit]:
    q = clean(query)
    e = enc(q)
    digits = digits_of(q)
    hits: list[Hit] = []
    hits += [
        Hit("Google", f"https://www.google.com/search?q=\"{e}\"", "exact match"),
        Hit("Bing", f"https://www.bing.com/search?q=\"{e}\"", "exact match"),
        Hit("DuckDuckGo", f"https://duckduckgo.com/?q=\"{e}\"", "exact match"),
        Hit("Yandex", f"https://yandex.com/search/?text=\"{e}\"", "faces/images"),
        Hit("Brave", f"https://search.brave.com/search?q=\"{e}\"", ""),
        Hit("Google Images", f"https://www.google.com/search?tbm=isch&q=\"{e}\"", ""),
        Hit("Bing Images", f"https://www.bing.com/images/search?q=\"{e}\"", ""),
        Hit("Yandex Images", f"https://yandex.com/images/search?text={e}", "best face recall"),
        Hit("WebMii", f"https://webmii.com/people?n=\"{e}\"", "people aggregator"),
        Hit("Social-Searcher", f"https://www.social-searcher.com/search-users/?q6={e}", "social mentions"),
        Hit("IntelX", f"https://intelx.io/?s={e}", "breach/paste index"),
        Hit("GitHub Code", f"https://github.com/search?q=%22{enc(q)}%22&type=code", "leaks in code"),
        Hit("Google Docs", f"https://www.google.com/search?q=\"{e}\"+filetype%3Apdf+OR+filetype%3Adoc+OR+filetype%3Axls", ""),
        Hit("Google Maps", f"https://www.google.com/maps/search/{e}", "business footprint"),
    ]
    if is_username(q):
        u = q.lstrip("@")
        ue = enc(u)
        for site in ["github.com", "x.com", "instagram.com", "tiktok.com", "reddit.com/user", "facebook.com", "linkedin.com/in", "youtube.com/@", "twitch.tv"]:
            hits.append(Hit(f"site:{site}", f"https://www.google.com/search?q=site%3A{enc(site)}+\"{ue}\"", "username footprint"))
        hits += [Hit("GitHub", f"https://github.com/{ue}", ""), Hit("X", f"https://x.com/{ue}", ""),
                 Hit("Instagram", f"https://instagram.com/{ue}", ""), Hit("TikTok", f"https://tiktok.com/@{ue}", ""),
                 Hit("Reddit", f"https://reddit.com/user/{ue}", ""), Hit("Namechk", f"https://namechk.com/{ue}/", "taken check")]
    if is_email(q):
        hits += [Hit("Epieos", f"https://epieos.com/?q={e}", "google account/reviews"),
                 Hit("HaveIBeenPwned", "https://haveibeenpwned.com/account/breach/", f"paste: {q}")]
    if is_phone(q) or digits:
        hits += [Hit("Truecaller", f"https://www.truecaller.com/search/{enc(digits)}", "caller id"),
                 Hit("SyncMe", f"https://sync.me/search/?number={enc(digits)}", ""),
                 Hit("ThatsThem", f"https://thatsthem.com/phone/{enc(digits)}", ""),
                 Hit("WhatsApp", f"https://wa.me/{digits}", "photo/about if public"),
                 Hit("Number-Reuse", f"https://www.google.com/search?q=\"{enc(digits)}\"+viber+OR+whatsapp+OR+telegram", "")]
    return hits
