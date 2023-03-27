import cv2
from pyzbar import pyzbar
import sqlite3
from flask import Flask, render_template, request

# Flask-App erstellen
app = Flask(__name__)

# Verbindung zur Datenbank herstellen
conn = sqlite3.connect("qr_codes.db")
cursor = conn.cursor()

# Index-Seite der App
@app.route("/")
def index():
    return render_template("index.html")

# Seite zum Scannen des QR-Codes
@app.route("/scan_qr")
def scan_qr():
    return render_template("scan_qr.html")

# QR-Code-Scanner
@app.route("/scan_qr_action")
def scan_qr_action():
    # Auf die Kamera zugreifen
    cap = cv2.VideoCapture(0)

    # Ein Bild von der Kamera aufnehmen
    ret, frame = cap.read()

    # QR-Codes aus dem Bild extrahieren
    decoded_objects = pyzbar.decode(frame)

    # QR-Codes durchlaufen und die Datenbank nach den Informationen durchsuchen
    for obj in decoded_objects:
        qr_data = obj.data.decode('utf-8')
        print("QR code data:", qr_data)
        cursor.execute("SELECT * FROM customers WHERE qr_code=?", (qr_data,))
        result = cursor.fetchone()
        if result:
            print("Customer information:")
            print("First name:", result[1])
            print("Last name:", result[2])
            print("Address:", result[3])
            return render_template("customer_info.html", first_name=result[1], last_name=result[2], address=result[3])
        else:
            print("No information found for this QR code.")
            return render_template("no_info.html")

    # Verbindung zur Datenbank schließen und Kamera freigeben
    conn.close()
    cap.release()
    cv2.destroyAllWindows()

# App ausführen
if __name__ == "__main__":
    app.run(debug=True)