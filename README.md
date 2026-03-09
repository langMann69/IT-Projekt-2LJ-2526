# Hotline-Wissensdatenbank

Dieses Projekt ist ein einfaches Konsolenprogramm in Python zur Verwaltung einer Wissensdatenbank für Hotline-Mitarbeiter.

Mitarbeiter können Fragen mit Lösungen speichern, durchsuchen, bearbeiten und löschen.  
Die Daten werden in einer JSON-Datei gespeichert.

Das Programm ist plattformunabhängig und läuft sowohl auf **Windows** als auch auf **macOS**.

---

# Funktionen

Das Programm erfüllt folgende User Stories:

**US1 – Frage speichern**  
Hotline-Mitarbeiter können eine Frage mit einer Lösung eingeben und speichern.

**US2 – Fragen suchen**  
Es kann nach einem Suchbegriff gesucht werden, um passende Fragen und Lösungen schnell zu finden.

**US3 – Frage bearbeiten**  
Bereits gespeicherte Fragen und Lösungen können geändert werden.

**US4 – Frage löschen**  
Nicht mehr relevante Fragen können gelöscht werden.

**US5 – Eingabemaske**  
Alle Funktionen sind über ein einfaches Konsolenmenü erreichbar.

---

# Projektstruktur


hotline-projekt/
│
├── main.py # Startpunkt des Programms
├── database.py # Laden und Speichern der Datenbank
├── hotline_service.py # Logik der Hotline-Funktionen
├── datenbank.json # gespeicherte Fragen und Lösungen
└── README.md


---

# Voraussetzungen

- Python **3.x**
- funktionierendes Terminal / Konsole

Python Version prüfen:


python3 --version


---

# Projekt starten

1. Repository klonen


git clone <repository-url>


2. In den Projektordner wechseln


cd hotline-projekt


3. Programm starten

macOS / Linux:


python3 main.py


Windows:


python main.py


---

# Bedienung des Programms

Nach dem Start erscheint ein Menü:

========================================
Hotline-Wissensdatenbank

1 - Neue Frage speichern
2 - Frage suchen
3 - Frage bearbeiten
4 - Frage löschen
5 - Alle Fragen anzeigen
0 - Programm beenden


### Neue Frage speichern

Der Benutzer gibt eine Frage und eine Lösung ein.  
Diese wird anschließend in der Datei `datenbank.json` gespeichert.

---

### Fragen suchen

Es kann ein Suchbegriff eingegeben werden.  
Alle passenden Fragen und Lösungen werden angezeigt.

---

### Frage bearbeiten

Eine bestehende Frage kann über ihre ID ausgewählt und verändert werden.

---

### Frage löschen

Eine gespeicherte Frage kann über ihre ID gelöscht werden.

---

### Alle Fragen anzeigen

Zeigt alle gespeicherten Fragen und Lösungen aus der Datenbank.

---

# Datenbank

Die Daten werden in der Datei


datenbank.json


gespeichert.

Beispiel:


{
"id": 1,
"frage": "Drucker druckt nicht",
"loesung": "Treiber neu installieren"
}