# Pacman

## Ziele
    - QR-Code Generierung
      - eigenes Backend (Dummy) zum Testen erstellen --> Datenbank erstellen
    - Informationen aus einem QR-Code lesen
      - mit Notebook-Kamera
 
### Ziel 23.03.2023
    - Fertiger QR-Code Generator
    
### Ziel 30.03.2023
    - Fertiger QR-Code Scanner
    
## Features
    - Ein QR-Code muss generiert werden
        - Lagerplatz muss zugewiesen werden (Daten von Datenbank)
    - Aus einem QR-Code müssen Informationen gelesen werden
    
## Test-Datenmodell
Für Testzwecke wird vorweg dieses Datenmodell verwendet.

![datamodel](https://github.com/denisepostl/pacman/blob/main/Test_Datenmodell.png)
    
## Dokumentation
[Entwicklerdokumentation](https://github.com/denisepostl/pacman/blob/main/docs/developer_doc.md) <br> 
[Benutzerdokumentation](https://github.com/denisepostl/pacman/blob/main/docs/user_doc.md)

## Pflichtenheft
Das Pflichtenheft befindet sich im [Dokumentationsordner](https://github.com/denisepostl/pacman/blob/main/docs/Pflichtenheft.pdf)

## API Schnittstellen-Überlegung
Wir haben uns für das Python-Webframework Flask entschieden.

### API QR-Generator

@app.route("/", methods=["GET", "POST"]) 
def index():
    Formulardaten lesen, in der Datenbank speichern, einen QR-Code generieren und PDF erstellen.

### API QR-Scanner

@app.route("/", methods=["GET", "POST"]) <br>
def index(): <br>
    return render_template("index.html") //Die "Main-Page" soll retourniert werden
    
@app.route("/results") <br>
def results(): <br>
    QR-Code von Bild lesen, nach passenden Eintrag in einer Datenbank suchen und Ergebnisse auf einer anderen Page retournieren
    

## Applikaiton
Welche Daten würden wir brauchen?
- Wir würden für unseren QR-Code Scanner die notwendigen Daten brauchen, die der Benutzer eingibt. Dafür könnten wir ein Formular erstellen und die eingegebenen Daten in der Datenbank speichern. Damit wir zur Datenbank kommen, würden wir eine API des Datenbank-Projektes benötigen und müssten diese in unserem Code einbinden und unsere Test-Datenbank löschen.
- Für unseren QR-Generator brauchen wir wieder eine Anbindung zur Datenbank. Wir müssten die API des Datenbank-Projektes wieder einbinden und so haben wir zugriff auf alle Daten in der Datenbank. 

Folgende Daten könnten wir brauchen:

    - Postoffice (ID, Location_ID)
    - Warehouse (ID, Location_ID)
    - Person (ID, First_Name, Last_Name)
    - Adress (ID, PostCode, City, Street, )
    - Phone (ID, Phone)
    - Location (ID, Adress_ID, Coords)
    - QR_Code (ID, QR_Code)
    - Package (ID, Name, Description, QR_Code_ID)
    


