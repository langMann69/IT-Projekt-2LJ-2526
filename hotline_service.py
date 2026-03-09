from database import lade_daten, speichere_daten


def naechste_id(daten):
    """Ermittelt die nächste freie ID."""
    if not daten:
        return 1
    return max(eintrag["id"] for eintrag in daten) + 1


def frage_hinzufuegen():
    """Fügt eine neue Frage mit Lösung hinzu."""
    print("\n--- Neue Frage hinzufügen ---")
    frage = input("Frage: ").strip()
    loesung = input("Lösung: ").strip()

    if not frage or not loesung:
        print("Frage und Lösung dürfen nicht leer sein.")
        return

    daten = lade_daten()
    eintrag = {
        "id": naechste_id(daten),
        "frage": frage,
        "loesung": loesung
    }
    daten.append(eintrag)
    speichere_daten(daten)

    print("Eintrag wurde erfolgreich gespeichert.")


def alle_fragen_anzeigen():
    """Zeigt alle gespeicherten Fragen mit Lösungen an."""
    print("\n--- Alle gespeicherten Fragen ---")
    daten = lade_daten()

    if not daten:
        print("Es sind keine Einträge vorhanden.")
        return

    for eintrag in daten:
        print(f"\nID: {eintrag['id']}")
        print(f"Frage: {eintrag['frage']}")
        print(f"Lösung: {eintrag['loesung']}")


def frage_suchen():
    """Sucht nach Fragen anhand eines Suchbegriffs."""
    print("\n--- Frage suchen ---")
    suchbegriff = input("Suchbegriff: ").strip().lower()

    if not suchbegriff:
        print("Bitte einen Suchbegriff eingeben.")
        return

    daten = lade_daten()
    treffer = []

    for eintrag in daten:
        if suchbegriff in eintrag["frage"].lower() or suchbegriff in eintrag["loesung"].lower():
            treffer.append(eintrag)

    if not treffer:
        print("Keine passenden Einträge gefunden.")
        return

    print(f"\n{len(treffer)} Treffer gefunden:")
    for eintrag in treffer:
        print(f"\nID: {eintrag['id']}")
        print(f"Frage: {eintrag['frage']}")
        print(f"Lösung: {eintrag['loesung']}")


def frage_bearbeiten():
    """Bearbeitet eine bestehende Frage mit Lösung."""
    print("\n--- Frage bearbeiten ---")
    daten = lade_daten()

    if not daten:
        print("Es sind keine Einträge vorhanden.")
        return

    alle_fragen_anzeigen()

    try:
        eintrag_id = int(input("\nID der zu bearbeitenden Frage: ").strip())
    except ValueError:
        print("Ungültige Eingabe. Bitte eine Zahl eingeben.")
        return

    for eintrag in daten:
        if eintrag["id"] == eintrag_id:
            print("\nAktuelle Daten:")
            print(f"Frage: {eintrag['frage']}")
            print(f"Lösung: {eintrag['loesung']}")

            neue_frage = input("Neue Frage (leer lassen = alte behalten): ").strip()
            neue_loesung = input("Neue Lösung (leer lassen = alte behalten): ").strip()

            if neue_frage:
                eintrag["frage"] = neue_frage
            if neue_loesung:
                eintrag["loesung"] = neue_loesung

            speichere_daten(daten)
            print("Eintrag wurde erfolgreich bearbeitet.")
            return

    print("Keine Frage mit dieser ID gefunden.")


def frage_loeschen():
    """Löscht eine gespeicherte Frage mit Lösung."""
    print("\n--- Frage löschen ---")
    daten = lade_daten()

    if not daten:
        print("Es sind keine Einträge vorhanden.")
        return

    alle_fragen_anzeigen()

    try:
        eintrag_id = int(input("\nID der zu löschenden Frage: ").strip())
    except ValueError:
        print("Ungültige Eingabe. Bitte eine Zahl eingeben.")
        return

    for eintrag in daten:
        if eintrag["id"] == eintrag_id:
            bestaetigung = input(
                f"Möchtest du die Frage '{eintrag['frage']}' wirklich löschen? (j/n): "
            ).strip().lower()

            if bestaetigung == "j":
                daten.remove(eintrag)
                speichere_daten(daten)
                print("Eintrag wurde erfolgreich gelöscht.")
            else:
                print("Löschen abgebrochen.")
            return

    print("Keine Frage mit dieser ID gefunden.")