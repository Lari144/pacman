from flask import Flask, render_template
import cv2
import numpy as np
from pyzbar import pyzbar
import sqlite3

app = Flask(__name__)

def decode_qr_code(image):
    barcodes = pyzbar.decode(image)
    for barcode in barcodes:
        if barcode.type == 'QRCODE':
            return barcode.data.decode('utf-8')
    return None

def query_database(qr_code_description):
    connection = sqlite3.connect('qr_codes.db')
    cursor = connection.cursor()

    cursor.execute("""
    SELECT 
	customers.First_Name, 
	customers.Last_Name, 
	products.description AS 'Produktbeschreibung', 
	products.order_date, 
	qr_codes.description AS 'QR-Beschreibung', 
	locations.description AS 'Standort'
    FROM qr_codes
    JOIN products 
	    ON qr_codes.product_id = products.product_id
    JOIN customers 
	    ON products.customer_id = customers.customer_id
    LEFT JOIN locations 
	    ON products.product_id = locations.product_id
	
    WHERE qr_codes.description = ?
    """, (qr_code_description,))

    results = cursor.fetchall()

    connection.close()

    return results

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/results")
def results():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        qr_code_data = decode_qr_code(frame)

        if qr_code_data:
            cap.release()
            cv2.destroyAllWindows()

            database_result = query_database(qr_code_data)

            if database_result:
                return render_template("results.html", results=database_result)
            else:
                return "No matching records found in the database."

            break
        else:
            cv2.imshow("QR Code Scanner", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    app.run(debug=True)