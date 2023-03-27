import cv2
import numpy as np
from pyzbar import pyzbar
from PIL import ImageGrab
import sqlite3

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

def main():
    
    screenshot = ImageGrab.grab()
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    qr_code_data = decode_qr_code(screenshot_cv)
    
    if qr_code_data:
        
        database_result = query_database(qr_code_data)
        
        if database_result:
            print("Database records:")
            for record in database_result:
                print("Customers id: ", record[0])
                print("Customers first name:", record[1])
                print("Custumers last name: ", record[2])
                print("Custumers Adress: ", record[3])
                print("Product id: ", record[4])
                print("Order-date: ", record[6])
                print("Order description: ", record[7])
                print("Location id:", record[12])
                print("Location description:", record[13])
                print("Qr id: ", record[8])
                print("Qr description:", record[10])
        else:
            print("No matching records found in the database.")
    else:
        print("No QR code detected in the screenshot.")

if __name__ == "__main__":
    main()
