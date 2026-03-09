import json
from pathlib import Path

DATEIPFAD = Path(__file__).parent / "datenbank.json"


def lade_daten():
    """Lädt alle Einträge aus der JSON-Datei."""
    if not DATEIPFAD.exists():
        return []

    try:
        with open(DATEIPFAD, "r", encoding="utf-8") as datei:
            inhalt = datei.read().strip()
            if not inhalt:
                return []
            return json.loads(inhalt)
    except (json.JSONDecodeError, OSError):
        print("Fehler beim Laden der Datenbank. Es wird mit einer leeren Liste gearbeitet.")
        return []


def speichere_daten(daten):
    """Speichert alle Einträge in der JSON-Datei."""
    try:
        with open(DATEIPFAD, "w", encoding="utf-8") as datei:
            json.dump(daten, datei, indent=4, ensure_ascii=False)
    except OSError:
        print("Fehler beim Speichern der Datenbank.")