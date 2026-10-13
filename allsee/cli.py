import argparse, sys, webbrowser, json
from allsee.engines import build_targets
from allsee.live import live_checks
from allsee.report import save_json, save_html
from allsee.utils import classify
from allsee.photo import file_info, reverse_links

def main():
    ap = argparse.ArgumentParser(prog="allsee", description="AllSee OSINT sweeper - public sources only")
    ap.add_argument("query", nargs="*", default=[], help="name / @username / phone / email / anything (spaces ok, no quotes needed)")
    ap.add_argument("--photo", default=None, help="local image file for reverse search + hash/exif")
    ap.add_argument("--image-url", default=None, help="public image url for uploadbyurl reverse search")
    ap.add_argument("--open", action="store_true", help="open top 12 links in browser")
    ap.add_argument("--json", default=None, help="save json path")
    ap.add_argument("--html", default=None, help="save html path")
    args = ap.parse_args()
    if args.photo:
        info = file_info(args.photo)
        print(json.dumps(info, indent=2))
        for l in reverse_links(image_url=args.image_url or "", local_hint=args.photo):
            print(f"[{l['source']}] {l['url']}")
        if args.open:
            for l in reverse_links(image_url=args.image_url or ""):
                try: webbrowser.open(l["url"])
                except: pass
        return
    if args.image_url and not args.query:
        for l in reverse_links(image_url=args.image_url):
            print(f"[{l['source']}] {l['url']}")
        return
    q = " ".join(args.query)
    print(f"[+] query: {q}  type: {classify(q)}")
    live = live_checks(q)
    print(f"[*] live: {live}")
    hits = build_targets(q)
    for i, h in enumerate(hits, 1):
        print(f"{i:02d}. [{h.source}] {h.note}\n    {h.url}")
    if args.json:
        save_json(hits, live, q, args.json)
        print(f"[+] saved -> {args.json}")
    if args.html:
        save_html(hits, live, q, args.html)
        print(f"[+] saved -> {args.html}")
    if args.open:
        for h in hits[:12]:
            try: webbrowser.open(h.url)
            except: pass

if __name__ == "__main__":
    main()
