import pytest
import io
import base64
from PyPDF2 import PdfFileReader
from PIL import Image
from QR_Code_Generator import app, create_tables

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    with app.test_client() as client:
        with app.app_context():
            # Create tables for test database
            create_tables()
        yield client

def test_index(client):
    """Test that the index page is accessible."""
    response = client.get("/")
    assert response.status_code == 200

def test_submit_form(client):
    """Test that the form submission generates a PDF with a QR code."""
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "address": "123 Main St",
        "order_date": "2023-04-13",
        "product_description": "Test product",
        "qr_description": "Test QR code",
        "location_description": "Test location"
    }
    response = client.post("/", data=data)
    assert response.status_code == 200
    # Check that the response is a PDF
    assert response.content_type == "application/pdf"
    # Check that the PDF contains the customer's name
    assert b"Name: John Doe" in response.data
    # Check that the PDF contains the product description
    assert b"Product Description: Test product" in response.data
    # Check that the PDF contains the QR description
    assert b"QR Description: Test QR code" in response.data
    # Check that the PDF contains the location description
    assert b"Location Description: Test location" in response.data
    # Check that the PDF contains a QR code image
    buffer = io.BytesIO(response.data)
    pdf = PdfFileReader(buffer)
    assert pdf.getNumPages() == 1
    page = pdf.getPage(0)
    xObject = page['/Resources']['/XObject'].getObject()
    assert len(xObject) == 1
    key = list(xObject.keys())[0]
    assert xObject[key]['/Subtype'] == '/Image'
    # Decode the base64 string and check that it is a valid image
    img_bytes = base64.b64decode(xObject[key]._data)
    assert Image.open(io.BytesIO(img_bytes)).format == "PNG"
