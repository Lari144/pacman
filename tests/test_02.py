import io
import os
import base64
import sqlite3
import qrcode
from fpdf import FPDF
from QR_Code_Generator.app import create_tables, generate_pdf

# Tests for create_tables function

def test_create_tables():
    # Connect to database and create tables
    conn = sqlite3.connect("test_qr_codes.db")
    cursor = conn.cursor()
    create_tables(cursor)
    # Check if tables were created successfully
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [table[0] for table in cursor.fetchall()]
    assert "customers" in tables
    assert "products" in tables
    assert "qr_codes" in tables
    assert "locations" in tables
    # Close connection to database and delete test database file
    conn.close()
    os.remove("test_qr_codes.db")


# Tests for generate_pdf function

def test_generate_pdf():
    # Create a sample QR code image
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    data = "Sample QR code"
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    # Save QR code image as base64 string
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    # Generate PDF with QR code image
    pdf_data = generate_pdf(qr_code_base64)
    assert isinstance(pdf_data, bytes)
    assert pdf_data.startswith(b"%PDF")
    # Delete temporary files
    os.remove("qr_code.png")
    os.remove("qr_code.pdf")