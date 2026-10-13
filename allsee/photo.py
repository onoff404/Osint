import os, hashlib, urllib.parse

def enc(q: str) -> str:
    return urllib.parse.quote_plus(q)

def file_info(path: str) -> dict:
    h = hashlib.md5()
    with open(path, "rb") as f:
        data = f.read()
        h.update(data)
    info = {"path": path, "bytes": len(data), "md5": h.hexdigest(),
            "sha256": hashlib.sha256(data).hexdigest()}
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS
        im = Image.open(path)
        info.update({"format": im.format, "size": list(im.size), "mode": im.mode})
        ex = {}
        raw = getattr(im, "_getexif", lambda: None)()
        if raw:
            for k, v in raw.items():
                ex[str(TAGS.get(k, k))] = str(v)[:200]
        info["exif"] = ex
    except Exception as ex:
        info["pil_error"] = str(ex)
    return info

def reverse_links(image_url: str = "", local_hint: str = "") -> list[dict]:
    links = []
    if image_url:
        e = enc(image_url)
        links += [
            {"source": "Google Lens (by URL)", "url": f"https://lens.google.com/uploadbyurl?url={e}"},
            {"source": "Bing Visual (paste URL)", "url": "https://www.bing.com/visualsearch"},
            {"source": "Yandex Images (paste URL)", "url": f"https://yandex.com/images/search?rpt=imageview&url={e}"},
            {"source": "TinEye (needs URL)", "url": f"https://tineye.com/search?url={e}"},
        ]
    else:
        links += [
            {"source": "Google Lens (upload file)", "url": "https://lens.google.com/"},
            {"source": "Bing Visual (upload file)", "url": "https://www.bing.com/visualsearch"},
            {"source": "Yandex Images (upload file)", "url": "https://yandex.com/images-apphost/image-download"},
            {"source": "TinEye (upload file)", "url": "https://tineye.com/"},
            {"source": "Pimeyes faces (upload)", "url": "https://pimeyes.com/en"},
            {"source": "FaceCheck faces (upload)", "url": "https://facecheck.id/"},
        ]
    if local_hint:
        links.append({"source": "note", "url": local_hint})
    return links
