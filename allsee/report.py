import json, html, datetime

def save_json(hits, live, query, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"query": query, "live": live, "hits": [h.__dict__ for h in hits]}, f, indent=2)

def save_html(hits, live, query, path):
    rows = "".join(f"<tr><td>{html.escape(h.source)}</td><td><a href='{html.escape(h.url)}'>{html.escape(h.url[:90])}</a></td><td>{html.escape(h.note)}</td></tr>" for h in hits)
    doc = f"""<html><head><meta charset='utf-8'><title>AllSee - {html.escape(query)}</title>
<style>body{{font-family:Arial;background:#0d1117;color:#e6edf3;padding:24px}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #30363d;padding:8px}}a{{color:#58a6ff}}pre{{background:#161b22;padding:12px}}</style></head>
<body><h1>AllSee report - {html.escape(query)}</h1><p>{datetime.datetime.now()}</p>
<h2>Live</h2><pre>{html.escape(json.dumps(live, indent=2))}</pre>
<h2>Links ({len(hits)})</h2><table><tr><th>Source</th><th>URL</th><th>Note</th></tr>{rows}</table></body></html>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(doc)
