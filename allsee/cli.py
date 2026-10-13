import argparse, sys, webbrowser
from allsee.engines import build_targets
from allsee.live import live_checks
from allsee.report import save_json, save_html
from allsee.utils import classify

def main():
    ap = argparse.ArgumentParser(prog="allsee", description="AllSee OSINT sweeper - public sources only")
    ap.add_argument("query", nargs="+", help="name / @username / phone / email / anything (spaces ok, no quotes needed)")
    ap.add_argument("--open", action="store_true", help="open top 12 links in browser")
    ap.add_argument("--json", default=None, help="save json path")
    ap.add_argument("--html", default=None, help="save html path")
    args = ap.parse_args()
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
