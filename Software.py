
#globale Variablen
pfad = "C:\\Users\\singdede\\OneDrive - B. Braun\\Dokumente\\Ausbildung\\schule\\AJ02\\Projekt\\Hotline.txt"

def schreiben(Pfad):
    #Dateipfad angeben Achtung immer doppelte \\ verwenden
    

    # Input in Datei speichern
    with open(Pfad, 'a') as datei:
        datei.write('Frage: ' + str(input("Frage: ")) + ',') # , als Trennung zwischen Frage und Lösung, wichtig für später
        datei.write('Lösung: ' + str(input("Lösung: ")) + ' \n')

def ausgeben(Pfad):
      #Datei ausgeben zum Vergleich
        with open(Pfad, 'r') as datei:
            for zeile in datei:
                print(zeile.strip())


schreiben(pfad)
ausgeben(pfad)


