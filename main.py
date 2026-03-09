from hotline_service import (
    frage_hinzufuegen,
    frage_suchen,
    frage_bearbeiten,
    frage_loeschen,
    alle_fragen_anzeigen
)


def menue_anzeigen():
    print("\n" + "=" * 40)
    print("   Hotline-Wissensdatenbank")
    print("=" * 40)
    print("1 - Neue Frage speichern")
    print("2 - Frage suchen")
    print("3 - Frage bearbeiten")
    print("4 - Frage löschen")
    print("5 - Alle Fragen anzeigen")
    print("0 - Programm beenden")


def main():
    while True:
        menue_anzeigen()
        auswahl = input("Bitte Auswahl eingeben: ").strip()

        if auswahl == "1":
            frage_hinzufuegen()
        elif auswahl == "2":
            frage_suchen()
        elif auswahl == "3":
            frage_bearbeiten()
        elif auswahl == "4":
            frage_loeschen()
        elif auswahl == "5":
            alle_fragen_anzeigen()
        elif auswahl == "0":
            print("Programm wird beendet. Auf Wiedersehen.")
            break
        else:
            print("Ungültige Auswahl. Bitte erneut versuchen.")


if __name__ == "__main__":
    main()