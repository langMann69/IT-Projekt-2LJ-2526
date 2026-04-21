import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from PIL import Image, ImageTk
from database import lade_daten, speichere_daten

# ── Dark-Blue Theme ───────────────────────────────────────────
BG          = "#0F1E2B"   # Haupthintergrund dunkelblau
BG2         = "#162533"   # etwas heller für Karten
ACCENT      = "#29ABE2"   # Sunfish-Blau
ACCENT_DARK = "#1A8FBF"
ROW_ODD     = "#1A2E3E"
ROW_EVEN    = "#162533"
TEXT        = "#E8F4FB"   # helles Weiß-Blau
SUBTEXT     = "#7BAEC8"   # gedämpftes Blau-Grau
BORDER      = "#1E3A50"
INPUT_BG    = "#1C3144"

LOGO_PFAD = Path(__file__).parent / "sunfish_logo.png"


def naechste_id(daten):
    return max((e["id"] for e in daten), default=0) + 1


class HotlineApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SunfishDesk – Hotline-Wissensdatenbank")
        self.configure(bg=BG)
        self.resizable(True, True)
        self._build()
        self.refresh()
        self.update_idletasks()
        # Fenster mittig auf dem Bildschirm platzieren
        w = self.winfo_width()
        h = self.winfo_height()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _build(self):
        # ── HEADER ───────────────────────────────────────────────
        hdr = tk.Frame(self, bg=BG2, pady=0)
        hdr.pack(fill="x")

        try:
            img = Image.open(LOGO_PFAD)
            h = 52
            w = int(img.width * h / img.height)
            # weißer Hintergrund → transparent machen für Dark Mode
            img = img.convert("RGBA")
            bg_img = Image.new("RGBA", img.size, BG2.lstrip("#"))
            # Logo einfach auf dunklem Hintergrund rendern
            img_rgb = Image.new("RGB", img.size, tuple(int(BG2[i:i+2], 16) for i in (1,3,5)))
            img_rgb.paste(img, mask=img.split()[3] if img.mode == "RGBA" else None)
            img_rgb = img_rgb.resize((w, h), Image.LANCZOS)
            self._logo = ImageTk.PhotoImage(img_rgb)
            tk.Label(hdr, image=self._logo, bg=BG2).pack(side="left", padx=20, pady=12)
        except Exception:
            tk.Label(hdr, text="SunfishDesk", font=("Helvetica Neue", 20, "bold"),
                     bg=BG2, fg=ACCENT).pack(side="left", padx=20, pady=12)

        tk.Frame(hdr, bg=BORDER, width=1).pack(side="left", fill="y", pady=8)
        tk.Label(hdr, text="Hotline-Wissensdatenbank",
                 font=("Helvetica Neue", 13), bg=BG2, fg=SUBTEXT
                 ).pack(side="left", padx=16)

        tk.Frame(self, bg=ACCENT, height=3).pack(fill="x")

        # ── SUCHLEISTE ───────────────────────────────────────────
        sf = tk.Frame(self, bg=BG, padx=20, pady=12)
        sf.pack(fill="x")

        tk.Label(sf, text="Suche", font=("Helvetica Neue", 11, "bold"),
                 bg=BG, fg=TEXT).pack(side="left", padx=(0, 8))

        self.such_var = tk.StringVar()
        self.such_var.trace_add("write", lambda *_: self.refresh())

        sf_box = tk.Frame(sf, bg=ACCENT, padx=1, pady=1)
        sf_box.pack(side="left")
        tk.Entry(sf_box, textvariable=self.such_var,
                 font=("Helvetica Neue", 11), width=50,
                 relief="flat", bd=7, bg=INPUT_BG,
                 fg=TEXT, insertbackground=ACCENT,
                 selectbackground=ACCENT).pack()

        # ── TABELLE ──────────────────────────────────────────────
        tf = tk.Frame(self, bg=BG, padx=20)
        tf.pack(fill="x")

        s = ttk.Style()
        s.theme_use("clam")
        s.configure("D.Treeview.Heading",
                    font=("Helvetica Neue", 11, "bold"),
                    background=ACCENT, foreground="#FFFFFF",
                    relief="flat", padding=(10, 7))
        s.configure("D.Treeview",
                    font=("Helvetica Neue", 11),
                    rowheight=32,
                    background=ROW_EVEN,
                    fieldbackground=ROW_EVEN,
                    foreground=TEXT,
                    borderwidth=0)
        s.map("D.Treeview",
              background=[("selected", ACCENT)],
              foreground=[("selected", "#FFFFFF")])
        s.configure("Blue.TButton",
                    background=ACCENT, foreground="#FFFFFF",
                    font=("Helvetica Neue", 11, "bold"),
                    padding=(20, 8), relief="flat", borderwidth=0)
        s.map("Blue.TButton",
              background=[("active", ACCENT_DARK), ("!active", ACCENT)],
              foreground=[("active", "#FFFFFF"),    ("!active", "#FFFFFF")])
        s.configure("Vertical.TScrollbar",
                    troughcolor=BG2, background=BORDER,
                    borderwidth=0, arrowsize=12)

        wrap = tk.Frame(tf, bg=BORDER, padx=1, pady=1)
        wrap.pack(fill="x")

        self.tree = ttk.Treeview(wrap, style="D.Treeview",
                                 columns=("id", "frage", "loesung"),
                                 show="headings", height=9,
                                 selectmode="browse")
        self.tree.heading("id",      text="ID")
        self.tree.heading("frage",   text="Frage")
        self.tree.heading("loesung", text="Lösung")
        self.tree.column("id",      width=50,  anchor="center", stretch=False)
        self.tree.column("frage",   width=370, stretch=False)
        self.tree.column("loesung", width=440, stretch=False)
        self.tree.tag_configure("even", background=ROW_EVEN)
        self.tree.tag_configure("odd",  background=ROW_ODD)
        self.tree.pack(side="left", fill="x")
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        sb = ttk.Scrollbar(wrap, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="left", fill="y")

        # ── EINGABE ───────────────────────────────────────────────
        ef = tk.Frame(self, bg=BG, padx=20, pady=14)
        ef.pack(fill="x")

        self.frage_var   = tk.StringVar()
        self.loesung_var = tk.StringVar()

        for row, (lbl, var) in enumerate([("Frage",  self.frage_var),
                                           ("Lösung", self.loesung_var)]):
            tk.Label(ef, text=lbl, font=("Helvetica Neue", 11, "bold"),
                     bg=BG, fg=TEXT, width=8, anchor="w"
                     ).grid(row=row, column=0, pady=6, sticky="w")

            box = tk.Frame(ef, bg=ACCENT, padx=1, pady=1)
            box.grid(row=row, column=1, pady=6, sticky="w")
            tk.Entry(box, textvariable=var,
                     font=("Helvetica Neue", 11), width=72,
                     relief="flat", bd=7, bg=INPUT_BG,
                     fg=TEXT, insertbackground=ACCENT,
                     selectbackground=ACCENT).pack()

        # ── BUTTONS ───────────────────────────────────────────────
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=20)

        bf = tk.Frame(self, bg=BG, padx=20, pady=14)
        bf.pack(fill="x")

        for text, cmd in [
            ("Hinzufügen", self.hinzufuegen),
            ("Bearbeiten", self.bearbeiten),
            ("Löschen",    self.loeschen),
            ("Leeren",     self.leeren),
        ]:
            ttk.Button(bf, text=text, command=cmd,
                       style="Blue.TButton").pack(side="left", padx=(0, 8))

    # ── Daten ─────────────────────────────────────────────────

    def refresh(self, *_):
        self.tree.delete(*self.tree.get_children())
        q = self.such_var.get().lower()
        for i, e in enumerate(lade_daten()):
            if q in e["frage"].lower() or q in e["loesung"].lower():
                self.tree.insert("", "end", iid=str(e["id"]),
                                 values=(e["id"], e["frage"], e["loesung"]),
                                 tags=("even" if i % 2 == 0 else "odd",))

    def _on_select(self, _=None):
        sel = self.tree.selection()
        if not sel:
            return
        v = self.tree.item(sel[0], "values")
        self.frage_var.set(v[1])
        self.loesung_var.set(v[2])

    def hinzufuegen(self):
        f, l = self.frage_var.get().strip(), self.loesung_var.get().strip()
        if not f or not l:
            messagebox.showwarning("Fehler", "Frage und Lösung dürfen nicht leer sein.")
            return
        daten = lade_daten()
        daten.append({"id": naechste_id(daten), "frage": f, "loesung": l})
        speichere_daten(daten)
        self.leeren(); self.refresh()

    def bearbeiten(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Hinweis", "Bitte zuerst einen Eintrag auswählen.")
            return
        f, l = self.frage_var.get().strip(), self.loesung_var.get().strip()
        if not f or not l:
            messagebox.showwarning("Fehler", "Frage und Lösung dürfen nicht leer sein.")
            return
        daten = lade_daten()
        for e in daten:
            if e["id"] == int(sel[0]):
                e["frage"] = f; e["loesung"] = l
        speichere_daten(daten)
        self.leeren(); self.refresh()

    def loeschen(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Hinweis", "Bitte zuerst einen Eintrag auswählen.")
            return
        if not messagebox.askyesno("Löschen", "Eintrag wirklich löschen?"):
            return
        speichere_daten([e for e in lade_daten() if e["id"] != int(sel[0])])
        self.leeren(); self.refresh()

    def leeren(self):
        self.frage_var.set("")
        self.loesung_var.set("")
        self.tree.selection_remove(self.tree.selection())


if __name__ == "__main__":
    HotlineApp().mainloop()
