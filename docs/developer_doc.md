# QR-Code Generator
Der Code für den QR-Code Generator befindet sich unter [QR_Code_Generator](https://github.com/denisepostl/pacman/tree/main/QR_Code_Generator) 

![QR_Code_Generator](https://github.com/denisepostl/pacman/blob/main/img/qr_code_generator.png)

Im Ordner Templates befindet sich die html-Datei für das Design des Generators. 
Das Programm für die Hauptfunktionalität befindet sich in [app.py](https://github.com/denisepostl/pacman/blob/main/QR_Code_Generator/app.py)


-----------------------------------------------------------------------------------------------------------------------------------------------------------
## Kurze Beschreibung der verwendeten Frameworks
Das Programm nutzt das Python-Webframework Flask, um eine Webseite zu erstellen, auf der QR-Codes generiert werden können und als PDF-Datei heruntergeladen werden. Dazu wird eine SQLite-Datenbank verwendet, um Kundendaten, Produktinformationen, Standortinformationen und QR-Code-Daten zu speichern.

Das Programm besteht aus einem Flask-Server, der auf die Eingabe von Formulardaten durch den Benutzer reagiert, die Daten in die Datenbank einfügt, einen QR-Code generiert und eine PDF-Datei mit dem QR-Code erstellt. Die PDF-Datei wird dann heruntergeladen.

## Entwicklungsumgebung
Um das Programm auszuführen, muss Python installiert sein und die notwendigen Bibliotheken wie Flask, qrcode, FPDF und sqlite3 installiert sein. Die Anwendung wird gestartet, indem man die Datei mit dem Python-Interpreter ausführt.

Dazu können Sie eine virtuelle Umgebung starten:
  - python -m venv venv
  - .\venv\Scripts\Activate.ps1

Anschließend können Sie die requirements installieren:
  - pip install -r requirements.txt

Wenn Sie die Bibliotheken bevorzugt manuell installieren möchten können Sie folgende Befehle verwenden:
  - pip install flask
  - pip install qrcode
  - pip install fpdf

Um das Programm zu starten können Sie in den Ordner QR_Code_Generator navigieren:
  - cd QR_Code_Generator

Anschließend können Sie das Programm [app.py](https://github.com/denisepostl/pacman/blob/main/QR_Code_Generator/app.py) ausführen:
  - python app.py

Sollte der flask Server nicht gestartet sein können Sie dies mit folgendem Befehl machen:
  - flask run 

Nun sollte der Server gestartet sein und unter der gegebenen IP-Adresse erreichbar: <br>
![IP-Adress](https://github.com/denisepostl/pacman/blob/main/img/server.png)

## Beschreibung des Codes
Das Programm besteht aus den folgenden Teilen:

Die Funktion *create_tables* erstellt alle notwendigen Tabellen in der SQLite-Datenbank, wenn sie noch nicht existieren. Die Funktion wird beim Start des Programms aufgerufen.

Die Funktion *generate_pdf* generiert eine PDF-Datei mit einem QR-Code und gibt das PDF-Dokument zurück. Die Funktion nimmt eine Base64-codierte Zeichenfolge entgegen, die den QR-Code enthält, und decodiert diese, um das Bild zu speichern. Das Bild wird in das PDF-Dokument eingebunden und das Dokument wird anschließend gedownloaded.

Die Flask-App hat nur eine Route /, auf die Anfragen per GET- oder POST-Methoden gesendet werden können. Das GET-Request rendert das Template *index.html*, während das POST-Request Formulardaten entgegennimmt und eine PDF-Datei mit einem QR-Code generiert.

Die Funktion *index* verarbeitet die Formulardaten, indem sie eine Verbindung zur SQLite-Datenbank aufbaut und die Daten in die entsprechenden Tabellen einfügt. Danach wird ein QR-Code mit den vom Benutzer eingegebenen Daten generiert und als Base64-codierte Zeichenfolge gespeichert. Schließlich wird die Funktion *generate_pdf* aufgerufen, um eine PDF-Datei mit dem QR-Code zu erstellen.

Der __main__-Aufruf des Programms prüft, ob das Skript als Hauptprogramm ausgeführt wird und ruft *create_tables* auf, um die Tabellen der Datenbank zu erstellen, falls sie noch nicht existieren. Danach wird die Flask-App gestartet und im Debug-Modus ausgeführt.

# QR-Code Scanner
Der Code für den QR-Code Scanner befindet sich unter [QR Code Scan](https://github.com/denisepostl/pacman/tree/main/QR_Code_Scan)
