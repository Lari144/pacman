from flask import Flask, render_template, request
import cv2
import numpy as np
from pyzbar import pyzbar
from PIL import ImageGrab
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
    SELECT customers.*, products.*, qr_codes.*, locations.*
    FROM qr_codes
    JOIN products ON qr_codes.product_id = products.product_id
    JOIN customers ON products.customer_id = customers.customer_id
    LEFT JOIN locations ON products.product_id = locations.product_id
    WHERE qr_codes.description = ?
    """, (qr_code_description,))

    results = cursor.fetchall()

    connection.close()

    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        screenshot = ImageGrab.grab()
        screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        qr_code_data = decode_qr_code(screenshot_cv)
        
        if qr_code_data:
            database_result = query_database(qr_code_data)
            
            if database_result:
                customers = []
                products = []
                locations = []
                qr_codes = []
                for record in database_result:
                    customers.append({
                        'id': record[0],
                        'first_name': record[1],
                        'last_name': record[2],
                        'address': record[3]
                    })
                    products.append({
                        'id': record[4],
                        'order_date': record[6],
                        'description': record[7]
                    })
                    if record[12] is not None:
                        locations.append({
                            'id': record[12],
                            'description': record[13]
                        })
                    qr_codes.append({
                        'id': record[8],
                        'description': record[10]
                    })
                return render_template('results.html', customers=customers, products=products, locations=locations, qr_codes=qr_codes)
            else:
                return render_template('error.html', message='No matching records found in the database.')
        else:
            return render_template('error.html', message='No QR code detected in the screenshot.')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
