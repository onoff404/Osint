import webbrowser, threading, json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from allsee.engines import build_targets
from allsee.live import live_checks
from allsee.report import save_json, save_html
from allsee.utils import classify
from allsee.photo import file_info, reverse_links

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AllSee OSINT")
        self.geometry("900x620")
        self.hits = []
        self.live = {}
        self.query = ""
        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")
        self.entry = ttk.Entry(top, font=("Segoe UI", 13))
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.entry.insert(0, "John Doe")
        self.entry.bind("<Return>", lambda e: self.run())
        ttk.Button(top, text="Search", command=self.run).pack(side="left")
        ttk.Button(top, text="Open Top 12", command=self.open_top).pack(side="left", padx=6)
        ttk.Button(top, text="Export HTML", command=self.export_html).pack(side="left")
        ttk.Button(top, text="Export JSON", command=self.export_json).pack(side="left", padx=6)
        ttk.Button(top, text="Photo...", command=self.photo).pack(side="left")
        self.info = ttk.Label(self, text="name / @username / phone / email", padding=(10, 0))
        self.info.pack(fill="x")
        mid = ttk.Panedwindow(self, orient="horizontal")
        mid.pack(fill="both", expand=True, padx=10, pady=6)
        left = ttk.Frame(mid)
        mid.add(left, weight=3)
        self.tree = ttk.Treeview(left, columns=("source", "note"), show="headings", height=20)
        self.tree.heading("source", text="Source")
        self.tree.heading("note", text="Note")
        self.tree.column("source", width=170)
        self.tree.column("note", width=260)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self.open_selected)
        right = ttk.Frame(mid)
        mid.add(right, weight=2)
        ttk.Label(right, text="Live / Details").pack(anchor="w")
        self.detail = tk.Text(right, wrap="word", height=25)
        self.detail.pack(fill="both", expand=True)
        self.status = ttk.Label(self, text="ready", padding=10)
        self.status.pack(fill="x")

    def run(self):
        q = self.entry.get().strip()
        if not q:
            return
        self.status.config(text="searching...")
        th = threading.Thread(target=self._work, args=(q,), daemon=True)
        th.start()

    def _work(self, q):
        self.query = q
        self.live = live_checks(q)
        self.hits = build_targets(q)
        self.after(0, self._paint)

    def _paint(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for h in self.hits:
            self.tree.insert("", "end", values=(h.source, h.note))
        self.detail.delete("1.0", "end")
        self.detail.insert("end", f"query: {self.query}  type: {classify(self.query)}\n\n")
        self.detail.insert("end", json.dumps(self.live, indent=2) + "\n\n")
        for i, h in enumerate(self.hits, 1):
            self.detail.insert("end", f"{i:02d}. [{h.source}] {h.url}\n")
        self.info.config(text=f"{classify(self.query)} - {len(self.hits)} links")
        self.status.config(text="done")

    def _url(self, idx):
        return self.hits[idx].url

    def open_selected(self, ev):
        sel = self.tree.selection()
        if not sel:
            return
        idx = self.tree.index(sel[0])
        webbrowser.open(self._url(idx))

    def open_top(self):
        for h in self.hits[:12]:
            webbrowser.open(h.url)

    def export_html(self):
        if not self.hits:
            return messagebox.showinfo("AllSee", "search first")
        p = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML", "*.html")])
        if p:
            save_html(self.hits, self.live, self.query, p)
            self.status.config(text=f"saved -> {p}")

    def export_json(self):
        if not self.hits:
            return messagebox.showinfo("AllSee", "search first")
        p = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if p:
            save_json(self.hits, self.live, self.query, p)
            self.status.config(text=f"saved -> {p}")

    def photo(self):
        p = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png *.webp *.bmp")])
        if not p:
            return
        info = file_info(p)
        self.detail.delete("1.0", "end")
        self.detail.insert("end", json.dumps(info, indent=2) + "\n\n")
        for i in self.tree.get_children():
            self.tree.delete(i)
        links = reverse_links()
        self.hits = []
        from allsee.engines import Hit
        for l in links:
            self.tree.insert("", "end", values=(l["source"], "upload the photo there"))
            self.hits.append(Hit(l["source"], l["url"], "reverse image upload"))
            self.detail.insert("end", f"[{l['source']}] {l['url']}\n")
        self.info.config(text=f"photo: {info.get('format')} {info.get('size')} md5={info.get('md5','')[:12]}")
        self.status.config(text="pick a source, upload the photo, double-click row to open")

def main():
    App().mainloop()

if __name__ == "__main__":
    main()
