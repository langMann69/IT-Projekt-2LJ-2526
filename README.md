
<img width="6912" height="3456" alt="Design ohne Titel (2)" src="https://github.com/user-attachments/assets/3297c43e-ed86-4339-b906-b7ab9916dbc6" />


# ThinkVault eine Hotline-Wissensdatenbank

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

<img alt="project_structure" src="https://github.com/user-attachments/assets/532ae30a-cff0-4bbf-af05-3d337c0a9460" />


---

# Voraussetzungen

- Python **3.x**
- funktionierendes Terminal / Konsole

Python Version prüfen:

```bash  
python3 --version
````

---

# Projekt starten

1. Repository klonen
```bash  
git clone https://github.com/langMann69/IT-Projekt-2LJ-2526.git
````



2. In den Projektordner wechseln
```bash  
cd hotline-projekt
````




3. Programm starten

macOS / Linux:
```bash  
python3 main.py
````




Windows:
```bash  
python main.py
````




---

# Bedienung des Programms

Nach dem Start erscheint ein Menü:<br> 

======================================== <br> 
Hotline-Wissensdatenbank <br> 
======================================== <br> 
1 - Neue Frage speichern <br> 
2 - Frage suchen <br> 
3 - Frage bearbeiten <br> 
4 - Frage löschen <br> 
5 - Alle Fragen anzeigen <br> 
0 - Programm beenden <br> 


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
