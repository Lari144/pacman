# QR-Code Generator

Beim Ausführen von [app.py](https://github.com/denisepostl/pacman/blob/main/QR_Code_Generator/app.py) mittels STRG+F5 wird der QR-Code Generator gestartet. Sie können nun
einen beliebiegen Browser öffnen und den Generator über den angegebenen Server erreichen. 

![Server](https://github.com/denisepostl/pacman/blob/main/img/server.png) <br>

## Eingabe der Daten
Nach starten des Servers und Aufruf im Browser sollten Sie folgenden Screen sehen können: <br>

![QR-Code](https://github.com/denisepostl/pacman/blob/main/img/QR_GENERATOR.png) <br>

Hier können Sie nun die Details des Pakets und des Kunden angeben.

## QR-Code Generieren
Wenn Sie alle Details eingegeben haben, könnnen Sie mittels Klick auf submit den QR-Code generieren: <br>
![Generate](https://github.com/denisepostl/pacman/blob/main/img/sub.png)
<br>

## QR-Code Downloaden
Der Download Ihres QR-Codes startet automatisch als PDF nach übermitteln des vollständig ausgefüllten Formulars: <br> <br>
![Downalod](https://github.com/denisepostl/pacman/blob/main/img/submit_pdf.png) <br>

# QR-Code Scanner
Der Flask Webserver kann auf gleiche Weise wie der QR-Code Generator gestartet werden. 

## QR-Code Scan
Mittels Klick auf Scan QR-Code wird Ihre Kamera gestartet.
![QR-Scan](https://github.com/denisepostl/pacman/blob/main/img/Scan_QR.png)

<br>
Nun können Sie den QR-Code einscannen und anschließend sollten die Informationen aus der Datenbank gelesen werden.
![QR-Scan-Ergebnis](https://github.com/denisepostl/pacman/blob/main/img/scan_result.png)
