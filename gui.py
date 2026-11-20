import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from PIL import Image, ImageTk
from database import lade_daten, speichere_daten

# ── Dark-Blue Theme ───────────────────────────────────────────
# Hier definieren wir alle Farben die wir im Programm verwenden als Konstanten.
# Das ist praktisch weil man so das gesamte Design an einem einzigen Ort ändern kann,
# anstatt jede Farbe überall einzeln raussuchen zu müssen.
# Tkinter akzeptiert Farben als Hex-Strings, genau wie in CSS beim Webdesign.
BG          = "#0F1E2B"   # Haupthintergrund dunkelblau
BG2         = "#162533"   # etwas heller für Karten
ACCENT      = "#29ABE2"   # Sunfish-Blau (der Markenfarbe)
ACCENT_DARK = "#1A8FBF"   # etwas dunkleres Blau für hover-Effekte auf Buttons
ROW_ODD     = "#1A2E3E"   # ungerade Tabellenzeilen (leicht heller damit man die Zeilen besser unterscheiden kann)
ROW_EVEN    = "#162533"   # gerade Tabellenzeilen
TEXT        = "#E8F4FB"   # helles Weiß-Blau für normalen Text
SUBTEXT     = "#7BAEC8"   # gedämpftes Blau-Grau für weniger wichtige Texte wie Untertitel
BORDER      = "#1E3A50"   # Farbe für Rahmenlinien und Trennstriche
INPUT_BG    = "#1C3144"   # Hintergrundfarbe der Eingabefelder

# Pfad zum Logo-Bild - Path(__file__).parent bedeutet "der Ordner in dem diese Python-Datei liegt"
# So funktioniert der Pfad auf jedem Rechner, egal wo das Projekt gespeichert ist
LOGO_PFAD = Path(__file__).parent / "sunfish_logo.png"


def naechste_id(daten):
    # Diese Funktion berechnet welche ID der nächste neue Eintrag bekommen soll.
    # Wir schauen einfach was die höchste vorhandene ID ist und addieren 1 drauf.
    # Das "default=0" beim max() ist wichtig: wenn die Datenbank komplett leer ist
    # würde max() normalerweise einen Fehler werfen weil es nichts zum vergleichen hat.
    # Mit default=0 gibt es in dem Fall einfach 0 zurück, und wir addieren 1 -> erster Eintrag bekommt ID 1.
    # Der Ausdruck in den Klammern ist ein sogenannter Generator: er geht durch alle Einträge
    # und zieht jeweils nur die "id" raus, ohne eine neue Liste im Speicher anzulegen.
    return max((e["id"] for e in daten), default=0) + 1


class HotlineApp(tk.Tk):
    # Das ist die Hauptklasse unserer Anwendung.
    # Wichtig: sie erbt von tk.Tk, das bedeutet die Klasse IST das Hauptfenster.
    # Das ist ein typisches Muster in Tkinter - man baut die ganze App als eine Klasse
    # damit alle Methoden (Funktionen) und alle Widgets (Fensterelemente) zusammen organisiert sind
    # und sich gegenseitig über "self" erreichen können.

    def __init__(self):
        # __init__ wird automatisch aufgerufen wenn man HotlineApp() schreibt.
        # Hier wird alles initializiert: zuerst das Fenster selbst (über super().__init__()),
        # dann der Titel und die Hintergrundfarbe gesetzt,
        # dann werden mit _build() alle Buttons, Felder und die Tabelle gebaut,
        # dann werden mit refresh() die gespeicherten Daten aus der Datenbank geladen und angezeigt.
        # Am Ende wird das Fenster noch schön mittig auf dem Bildschirm platziert.
        super().__init__()
        self.title("SunfishDesk – Hotline-Wissensdatenbank")
        self.configure(bg=BG)
        self.resizable(True, True)
        self._build()
        self.refresh()

        # update_idletasks() ist notwendig damit Tkinter die echte Fenstergröße berechnet
        # bevor wir sie auslesen. Ohne diesen Aufruf wären winfo_width() und winfo_height()
        # noch 1x1 Pixel weil Tkinter das Fenster noch nicht wirklich gezeichnet hat.
        self.update_idletasks()

        # Fenster mittig auf dem Bildschirm platzieren:
        # winfo_width/height = aktuelle Fenstergröße
        # winfo_screenwidth/height = gesamte Bildschirmauflösung
        # Die geometry-Methode nimmt das Format "BreitexHöhe+X+Y" wobei X und Y
        # die Position der oberen linken Ecke des Fensters auf dem Bildschirm sind
        w = self.winfo_width()
        h = self.winfo_height()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _build(self):
        # Diese Methode baut die gesamte Benutzeroberfläche auf.
        # In Tkinter gibt es verschiedene sogenannte "Layout-Manager" die bestimmen
        # wie Elemente im Fenster angeordnet werden:
        #   .pack()  → stapelt Elemente einfach untereinander oder nebeneinander
        #   .grid()  → ordnet Elemente in einem Raster aus Zeilen und Spalten an
        #   .place() → absolute Pixelpositionierung (hier nicht verwendet)
        # WICHTIG: Man darf pack() und grid() NICHT im selben Frame mischen,
        # sonst stürzt Tkinter ab!

        # ── HEADER ───────────────────────────────────────────────
        # Der Header ist ein tk.Frame - das ist ein unsichtbarer Container der andere Widgets gruppiert.
        # fill="x" bedeutet: strecke den Frame über die volle Fensterbreite
        hdr = tk.Frame(self, bg=BG2, pady=0)
        hdr.pack(fill="x")

        # Hier versuchen wir das Logo-Bild zu laden.
        # Wir verwenden Pillow (PIL) weil das normale Tkinter nur GIF und PPM unterstützt,
        # aber kein PNG. Mit Pillow können wir jedes Bildformat laden.
        # Der try/except-Block stellt sicher dass das Programm nicht abstürzt wenn das Logo fehlt -
        # in dem Fall wird einfach ein Text als Ersatz angezeigt. Das nennt man "graceful degradation".
        try:
            img = Image.open(LOGO_PFAD)
            h = 52  # Zielhöhe in Pixeln
            w = int(img.width * h / img.height)  # Breite proportional berechnen (Seitenverhältnis beibehalten)

            # Das Logo hat einen weißen Hintergrund - wir konvertieren es zu RGBA (mit Alphakanal = Transparenz)
            # und rendern es dann auf unserem dunklen Hintergrund, damit es sauber aussieht
            img = img.convert("RGBA")
            bg_img = Image.new("RGBA", img.size, BG2.lstrip("#"))
            img_rgb = Image.new("RGB", img.size, tuple(int(BG2[i:i+2], 16) for i in (1,3,5)))
            # paste() mit dem Alphakanal als Maske: transparente Pixel des Logos werden
            # durch den Hintergrund ersetzt, undurchsichtige Pixel bleiben erhalten
            img_rgb.paste(img, mask=img.split()[3] if img.mode == "RGBA" else None)
            img_rgb = img_rgb.resize((w, h), Image.LANCZOS)  # LANCZOS = hochwertige Skalierung

            # ImageTk.PhotoImage konvertiert das PIL-Bild in ein Tkinter-kompatibles Format.
            # Wichtig: wir speichern das Bild als self._logo - wenn wir es nur als lokale Variable
            # hätten, würde Python es sofort wieder löschen (Garbage Collection) und das Label
            # würde leer bleiben. Das ist eine häufige Fehlerquelle in Tkinter!
            self._logo = ImageTk.PhotoImage(img_rgb)
            tk.Label(hdr, image=self._logo, bg=BG2).pack(side="left", padx=20, pady=12)
        except Exception:
            # Fallback falls das Logo nicht gefunden wurde oder ein Fehler beim Laden auftrat
            tk.Label(hdr, text="SunfishDesk", font=("Helvetica Neue", 20, "bold"),
                     bg=BG2, fg=ACCENT).pack(side="left", padx=20, pady=12)

        # Vertikale Trennlinie zwischen Logo und Titel (width=1 macht sie hauchdünn)
        tk.Frame(hdr, bg=BORDER, width=1).pack(side="left", fill="y", pady=8)
        tk.Label(hdr, text="Hotline-Wissensdatenbank",
                 font=("Helvetica Neue", 13), bg=BG2, fg=SUBTEXT
                 ).pack(side="left", padx=16)

        # Horizontale Akzentlinie unter dem Header (height=3 = 3 Pixel dicker blauer Strich)
        tk.Frame(self, bg=ACCENT, height=3).pack(fill="x")

        # ── SUCHLEISTE ───────────────────────────────────────────
        # Ein Frame als Abstandshalter mit Innenabstand (padx, pady)
        sf = tk.Frame(self, bg=BG, padx=20, pady=12)
        sf.pack(fill="x")

        tk.Label(sf, text="Suche", font=("Helvetica Neue", 11, "bold"),
                 bg=BG, fg=TEXT).pack(side="left", padx=(0, 8))

        # tk.StringVar ist eine besondere Tkinter-Variable die man mit Widgets verbinden kann.
        # Wenn der Nutzer im Textfeld tippt, aktualisiert sich such_var automatisch.
        # Wenn Code such_var.set("...") aufruft, aktualisiert sich das Textfeld automatisch.
        # Das ist bidirektionale Datenbindung - ähnlich wie in modernen Web-Frameworks.
        self.such_var = tk.StringVar()

        # trace_add("write", ...) registriert eine Callback-Funktion die bei JEDER Änderung
        # der Variable aufgerufen wird. So wird die Tabelle live gefiltert während man tippt,
        # ohne dass man einen "Suchen"-Button drücken müsste.
        # Das lambda fängt die Argumente die trace übergibt auf (die wir nicht brauchen)
        # und ruft dann einfach self.refresh() auf.
        self.such_var.trace_add("write", lambda *_: self.refresh())

        # Kleiner Trick für den blauen Rahmen um das Eingabefeld:
        # Ein Frame mit ACCENT-Farbe und 1px Innenabstand umschließt das Entry.
        # Das Entry selbst hat keinen Rahmen (relief="flat"), dadurch sieht es so aus
        # als hätte das Entry einen blauen Rand - ist aber eigentlich der Frame dahinter.
        sf_box = tk.Frame(sf, bg=ACCENT, padx=1, pady=1)
        sf_box.pack(side="left")
        tk.Entry(sf_box, textvariable=self.such_var,
                 font=("Helvetica Neue", 11), width=50,
                 relief="flat", bd=7, bg=INPUT_BG,
                 fg=TEXT, insertbackground=ACCENT,   # insertbackground = Farbe des Cursors im Textfeld
                 selectbackground=ACCENT).pack()     # selectbackground = Farbe wenn Text markiert ist

        # ── TABELLE ──────────────────────────────────────────────
        tf = tk.Frame(self, bg=BG, padx=20)
        tf.pack(fill="x")

        # ttk.Style ist das Styling-System von ttk (themed tkinter - die modernere Widget-Bibliothek).
        # Mit "clam" als Basis-Theme haben wir die meiste Kontrolle über die Optik.
        # Wir definieren eigene Stile mit dem Präfix "D." (für Dark) die wir dann
        # bei den jeweiligen Widgets als style="D.Treeview" etc. angeben.
        s = ttk.Style()
        s.theme_use("clam")

        # Stil für die Spaltenüberschriften der Tabelle
        s.configure("D.Treeview.Heading",
                    font=("Helvetica Neue", 11, "bold"),
                    background=ACCENT, foreground="#FFFFFF",
                    relief="flat", padding=(10, 7))

        # Stil für die Tabellenzeilen selbst
        s.configure("D.Treeview",
                    font=("Helvetica Neue", 11),
                    rowheight=32,          # Zeilenhöhe in Pixeln
                    background=ROW_EVEN,
                    fieldbackground=ROW_EVEN,
                    foreground=TEXT,
                    borderwidth=0)

        # s.map() definiert zustandsabhängige Stile - also wie ein Widget aussieht
        # wenn es selected, hover, disabled etc. ist. Hier: ausgewählte Zeile = blauer Hintergrund
        s.map("D.Treeview",
              background=[("selected", ACCENT)],
              foreground=[("selected", "#FFFFFF")])

        # Stil für alle Buttons in der App
        s.configure("Blue.TButton",
                    background=ACCENT, foreground="#FFFFFF",
                    font=("Helvetica Neue", 11, "bold"),
                    padding=(20, 8), relief="flat", borderwidth=0)
        s.map("Blue.TButton",
              background=[("active", ACCENT_DARK), ("!active", ACCENT)],   # active = Maus darüber
              foreground=[("active", "#FFFFFF"),    ("!active", "#FFFFFF")])

        # Stil für die Scrollbar rechts von der Tabelle
        s.configure("Vertical.TScrollbar",
                    troughcolor=BG2, background=BORDER,
                    borderwidth=0, arrowsize=12)

        # Wieder der Rahmen-Trick: ein Frame mit BORDER-Farbe umschließt die Tabelle
        # um ihr einen sauberen Rahmen zu geben
        wrap = tk.Frame(tf, bg=BORDER, padx=1, pady=1)
        wrap.pack(fill="x")

        # ttk.Treeview ist eigentlich für Baumstrukturen gedacht (wie ein Dateiexplorer),
        # aber mit show="headings" verstecken wir die Baumstruktur und nutzen es als reine Tabelle.
        # columns=(...) definiert die internen Namen der Spalten (nicht die angezeigten Titel).
        # height=9 bedeutet: zeige 9 Zeilen gleichzeitig an (ohne Scrollen)
        # selectmode="browse" = nur eine Zeile kann gleichzeitig ausgewählt sein
        self.tree = ttk.Treeview(wrap, style="D.Treeview",
                                 columns=("id", "frage", "loesung"),
                                 show="headings", height=9,
                                 selectmode="browse")

        # Spaltenüberschriften setzen (das ist was der Nutzer sieht)
        self.tree.heading("id",      text="ID")
        self.tree.heading("frage",   text="Frage")
        self.tree.heading("loesung", text="Lösung")

        # Spaltenbreiten setzen. stretch=False verhindert dass sich die Spalte
        # automatisch verbreitert wenn das Fenster größer wird
        self.tree.column("id",      width=50,  anchor="center", stretch=False)
        self.tree.column("frage",   width=370, stretch=False)
        self.tree.column("loesung", width=440, stretch=False)

        # Tags für die abwechselnde Zeilenfärbung (Zebra-Muster) konfigurieren.
        # Die Tags werden beim Einfügen der Zeilen in refresh() zugewiesen.
        self.tree.tag_configure("even", background=ROW_EVEN)
        self.tree.tag_configure("odd",  background=ROW_ODD)
        self.tree.pack(side="left", fill="x")

        # Wenn der Nutzer eine Zeile anklickt, wird das Event <<TreeviewSelect>> ausgelöst.
        # Wir binden es an unsere _on_select Methode die dann die Felder befüllt.
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        # Scrollbar für die Tabelle erstellen und mit der Tabelle verknüpfen.
        # yscrollcommand und command verbinden Scrollbar und Treeview bidirektional:
        # die Scrollbar steuert die Tabelle, und die Tabelle sagt der Scrollbar wo sie gerade ist.
        sb = ttk.Scrollbar(wrap, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="left", fill="y")

        # ── EINGABE ───────────────────────────────────────────────
        ef = tk.Frame(self, bg=BG, padx=20, pady=14)
        ef.pack(fill="x")

        # StringVars für die Eingabefelder - gleicher Mechanismus wie bei der Suche.
        # Über diese Variablen können wir den Inhalt der Felder lesen und setzen.
        self.frage_var   = tk.StringVar()
        self.loesung_var = tk.StringVar()

        # Mit einer Schleife bauen wir beide Eingabefelder (Frage und Lösung) auf einmal.
        # Das ist effizienter als den gleichen Code zweimal zu schreiben (DRY-Prinzip).
        # enumerate() gibt uns automatisch einen Zähler (row=0, row=1) für das grid-Layout.
        # grid() ordnet die Widgets in einem Raster an: row=Zeile, column=Spalte
        for row, (lbl, var) in enumerate([("Frage",  self.frage_var),
                                           ("Lösung", self.loesung_var)]):
            tk.Label(ef, text=lbl, font=("Helvetica Neue", 11, "bold"),
                     bg=BG, fg=TEXT, width=8, anchor="w"
                     ).grid(row=row, column=0, pady=6, sticky="w")

            # Wieder der Rahmen-Trick für den blauen Rand ums Eingabefeld
            box = tk.Frame(ef, bg=ACCENT, padx=1, pady=1)
            box.grid(row=row, column=1, pady=6, sticky="w")
            tk.Entry(box, textvariable=var,
                     font=("Helvetica Neue", 11), width=72,
                     relief="flat", bd=7, bg=INPUT_BG,
                     fg=TEXT, insertbackground=ACCENT,
                     selectbackground=ACCENT).pack()

        # ── BUTTONS ───────────────────────────────────────────────
        # Horizontale Trennlinie über den Buttons
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=20)

        bf = tk.Frame(self, bg=BG, padx=20, pady=14)
        bf.pack(fill="x")

        # Alle vier Buttons werden wieder in einer Schleife erstellt.
        # Jeder Button bekommt einen Text und eine Funktion (command) die beim Klick aufgerufen wird.
        # side="left" und padx stapelt sie nebeneinander mit etwas Abstand dazwischen.
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
        # Diese Methode leert die Tabelle komplett und befüllt sie neu aus der Datenbank.
        # Sie wird aufgerufen wenn: die App startet, der Nutzer tippt (Suche), oder nach jeder Änderung.
        #
        # Zuerst alle vorhandenen Zeilen löschen:
        # get_children() gibt eine Liste aller Zeilen-IDs zurück,
        # der Stern vor self.tree.get_children() "entpackt" die Liste in einzelne Argumente
        # (also delete(zeile1, zeile2, ...) statt delete([zeile1, zeile2, ...]))
        self.tree.delete(*self.tree.get_children())

        # Suchbegriff auslesen und in Kleinbuchstaben umwandeln (für case-insensitive Suche)
        q = self.such_var.get().lower()

        # Alle Einträge aus der Datenbank laden und gefiltert in die Tabelle einfügen.
        # enumerate() gibt uns i=0,1,2,... für die Zebrfärbung (gerade/ungerade Zeilen)
        for i, e in enumerate(lade_daten()):
            # Suchfilter: nur anzeigen wenn der Suchbegriff in der Frage ODER der Lösung vorkommt
            if q in e["frage"].lower() or q in e["loesung"].lower():
                # iid=str(e["id"]) setzt die interne ID der Treeview-Zeile auf unsere Datenbank-ID.
                # Das ist wichtig damit wir beim Klick auf eine Zeile wissen welchen Eintrag sie hat.
                self.tree.insert("", "end", iid=str(e["id"]),
                                 values=(e["id"], e["frage"], e["loesung"]),
                                 tags=("even" if i % 2 == 0 else "odd",))

    def _on_select(self, _=None):
        # Wird aufgerufen wenn der Nutzer eine Zeile in der Tabelle anklickt.
        # Wir lesen die Werte der ausgewählten Zeile aus und schreiben sie
        # in die Eingabefelder - so kann der Nutzer einen Eintrag direkt bearbeiten.
        #
        # selection() gibt eine Liste der ausgewählten Zeilen-IDs zurück
        # (bei selectmode="browse" ist das immer maximal eine)
        sel = self.tree.selection()
        if not sel:
            return  # nichts ausgewählt, nichts tun

        # item(id, "values") gibt die Spaltenwerte der Zeile zurück: (id, frage, loesung)
        # v[0] = ID, v[1] = Frage, v[2] = Lösung
        v = self.tree.item(sel[0], "values")
        self.frage_var.set(v[1])
        self.loesung_var.set(v[2])

    def hinzufuegen(self):
        # Legt einen neuen Eintrag in der Datenbank an.
        # Ablauf: Eingaben lesen → validieren → Daten laden → neuen Eintrag anhängen → speichern → UI aktualisieren
        f, l = self.frage_var.get().strip(), self.loesung_var.get().strip()

        # .strip() entfernt Leerzeichen am Anfang und Ende - verhindert dass " " als gültiger Text gilt
        if not f or not l:
            messagebox.showwarning("Fehler", "Frage und Lösung dürfen nicht leer sein.")
            return

        daten = lade_daten()
        # Neuen Eintrag als Dictionary anlegen und an die Liste anhängen
        daten.append({"id": naechste_id(daten), "frage": f, "loesung": l})
        speichere_daten(daten)

        # Felder leeren und Tabelle neu laden um den neuen Eintrag anzuzeigen
        self.leeren()
        self.refresh()

    def bearbeiten(self):
        # Überschreibt den aktuell ausgewählten Eintrag mit den Werten aus den Eingabefeldern.
        # Erst prüfen ob überhaupt etwas ausgewählt ist - sonst wüssten wir nicht was wir bearbeiten sollen
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Hinweis", "Bitte zuerst einen Eintrag auswählen.")
            return

        f, l = self.frage_var.get().strip(), self.loesung_var.get().strip()
        if not f or not l:
            messagebox.showwarning("Fehler", "Frage und Lösung dürfen nicht leer sein.")
            return

        daten = lade_daten()

        # Durch alle Einträge iterieren und den mit der passenden ID finden und überschreiben.
        # int(sel[0]) weil sel[0] ein String ist (die Treeview-ID) aber e["id"] eine Zahl ist.
        for e in daten:
            if e["id"] == int(sel[0]):
                e["frage"] = f
                e["loesung"] = l

        speichere_daten(daten)
        self.leeren()
        self.refresh()

    def loeschen(self):
        # Löscht den ausgewählten Eintrag dauerhaft aus der Datenbank.
        # Erst Auswahl prüfen, dann sicherheitshalber nochmal nachfragen (damit man nicht aus versehen löscht),
        # dann den Eintrag rausfiltern und die bereinigte Liste speichern.
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Hinweis", "Bitte zuerst einen Eintrag auswählen.")
            return

        # askyesno zeigt ein Ja/Nein-Dialogfenster und gibt True oder False zurück
        if not messagebox.askyesno("Löschen", "Eintrag wirklich löschen?"):
            return  # Nutzer hat "Nein" geklickt, abbrechen

        # List Comprehension: neue Liste erstellen die alle Einträge AUSSER dem zu löschenden enthält.
        # Das ist kürzer und pythonischer als eine Schleife mit if/continue.
        speichere_daten([e for e in lade_daten() if e["id"] != int(sel[0])])
        self.leeren()
        self.refresh()

    def leeren(self):
        # Setzt die Eingabefelder auf leer zurück und hebt die Tabellenauswahl auf.
        # Wird nach jeder Aktion (hinzufügen, bearbeiten, löschen) aufgerufen
        # damit die Felder nicht mit alten Werten befüllt bleiben.
        self.frage_var.set("")
        self.loesung_var.set("")
        # selection_remove() nimmt eine Liste von Zeilen-IDs - wir übergeben die aktuell
        # ausgewählten Zeilen damit die Markierung verschwindet
        self.tree.selection_remove(self.tree.selection())


if __name__ == "__main__":
    # Dieser Block wird nur ausgeführt wenn man die Datei direkt startet (python gui.py).
    # Wenn gui.py von einer anderen Datei importiert wird, wird dieser Block NICHT ausgeführt.
    # Das ist ein Standard-Python-Muster.
    #
    # HotlineApp() erstellt die Anwendung und __init__ baut alles auf.
    # mainloop() startet die Ereignisschleife - das ist quasi das Herz von Tkinter.
    # Sie wartet endlos auf Nutzeraktionen (Klicks, Tastatureingaben), verarbeitet sie
    # und zeichnet das Fenster bei Bedarf neu. Sie läuft bis das Fenster geschlossen wird.
    HotlineApp().mainloop()
