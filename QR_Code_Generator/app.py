from flask import Flask, render_template, request, send_file
import sqlite3
import qrcode
import io
import base64
from fpdf import FPDF
import os

app = Flask(__name__)

def create_tables():
    """Create all tables for db."""
    conn = sqlite3.connect("qr_codes.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        First_Name TEXT NOT NULL,
        Last_Name TEXT NOT NULL,
        Address TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        order_date DATE NOT NULL,
        description TEXT NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS qr_codes (
        qr_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        description TEXT NOT NULL,
        qr_code TEXT NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products (product_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS locations (
        location_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        description TEXT NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products (product_id)
    )
    """)
    conn.commit()
    conn.close()

def generate_pdf(qr_code_base64, first_name, last_name, address, order_date, product_description, qr_description, location_description):
    """Generate PDF with QR-Code image and return the PDF document."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Decode base64 string and save the image as a file
    with open("qr_code.png", "wb") as fh:
        fh.write(base64.b64decode(qr_code_base64))
    pdf.image("qr_code.png", x=10, y=70, w=50)
    pdf.output("qr_code.pdf")

    # Add customer information to the PDF document
    pdf.cell(200, 10, txt=f"Name: {first_name} {last_name}", ln=1)
    pdf.cell(200, 10, txt=f"Address: {address}", ln=1)
    
    # Add product information to the PDF document
    pdf.cell(200, 10, txt=f"Order Date: {order_date}", ln=1)
    pdf.cell(200, 10, txt=f"Product Description: {product_description}", ln=1)
    
    # Add QR description to the PDF document
    pdf.cell(200, 10, txt=f"QR Description: {qr_description}", ln=1)
    
    # Add location description to the PDF document
    pdf.cell(200, 10, txt=f"Location Description: {location_description}", ln=1)
    
    # Delete the temporary image file
    os.remove("qr_code.png")
    return send_file("qr_code.pdf", as_attachment=True)

@app.route("/", methods=["GET", "POST"])
def index():
    # Check, if Formular has been sent
    if request.method == "POST":
        # Call Values of Formular
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        address = request.form["address"]
        order_date = request.form["order_date"]
        product_description = request.form["product_description"]
        qr_description = request.form["qr_description"]
        location_description = request.form["location_description"]

        # Connection to Database
        conn = sqlite3.connect("qr_codes.db")
        cursor = conn.cursor()

        # Insert the inserted Data for Customer in Table customers
        cursor.execute("INSERT INTO customers (First_Name, Last_Name, Address) VALUES (?, ?, ?)", #insert Data in customers
                   (first_name, last_name, address))
        customer_id = cursor.lastrowid

        # Insert the inserted Data for Product in Table products
        cursor.execute("INSERT INTO products (customer_id, order_date, description) VALUES (?, ?, ?)", 
                   (customer_id, order_date, product_description))
        product_id = cursor.lastrowid

        # Create QR-Code image
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        data = f"{product_description} | {qr_description}"
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Save QR-Code image as base64 string
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        cursor.execute("INSERT INTO qr_codes (product_id, description, qr_code) VALUES (?, ?, ?)",
                   (product_id, qr_description, qr_code_base64))

        # Insert the inserted Data for Location in Table locations
        cursor.execute("INSERT INTO locations (product_id, description) VALUES (?, ?)",
                   (product_id, location_description))

        # Commit and Close Connection to Database
        conn.commit()
        conn.close()

        # Generate and return PDF with QR-Code image
        return generate_pdf(qr_code_base64, first_name, last_name, address, order_date, product_description, qr_description, location_description)

    # If no form data has been sent, render the index template
    return render_template("index.html")

if __name__ == "main":
# Create tables for database if they do not exist
    create_tables()
# Start the Flask application
    app.run(debug=True)