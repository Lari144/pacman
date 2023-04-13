# Import necessary modules
from flask import Flask, render_template
import cv2
import numpy as np
from pyzbar import pyzbar
import sqlite3

# Create Flask application instance
app = Flask(__name__)

# Function to decode QR code from image
def decode_qr_code(image):
    barcodes = pyzbar.decode(image)  # Decode QR code
    for barcode in barcodes:
        if barcode.type == 'QRCODE':
            return barcode.data.decode('utf-8')
    return None

# Function to query database for QR code description
def query_database(qr_code_description):
    connection = sqlite3.connect('qr_codes.db')  # Connect to database
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
    """, (qr_code_description,))  # Execute SQL query with QR code description as parameter

    results = cursor.fetchall()  # Fetch query results

    connection.close()  # Close database connection

    return results

# Route to index page
@app.route("/")
def index():
    return render_template("index.html")

# Route to display results page
@app.route("/results")
def results():
    cap = cv2.VideoCapture(0)  # Start video capture

    while True:
        ret, frame = cap.read()  # Read frame from video capture

        if not ret:  # Exit if no frame is captured
            break

        qr_code_data = decode_qr_code(frame)  # Decode QR code from frame

        if qr_code_data:  # If QR code is decoded
            cap.release()  # Release video capture
            cv2.destroyAllWindows()  # Close all OpenCV windows

            database_result = query_database(qr_code_data)  # Query database for QR code description

            if database_result:  # If query returns a result
                return render_template("results.html", results=database_result)  # Display results page with query results
            else:  # If no result is found in database
                return "No matching records found in the database."

            break  # Exit loop

        else:  # If QR code is not decoded
            cv2.imshow("QR Code Scanner", frame)  # Display frame in OpenCV window
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit if 'q' key is pressed
                break

    cap.release()  # Release video capture
    cv2.destroyAllWindows()  # Close all OpenCV windows

if __name__ == "__main__":
    app.run(debug=True)  # Start Flask application in debug mode
