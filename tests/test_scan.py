import pytest
import cv2
from QR_Code_Scan import app, decode_qr_code, query_database

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to QR Code Scanner" in response.data

def test_results_page(client):
    # Assuming there is a QR code in the database with description "Test QR Code"
    response = client.get("/results?q=Test%20QR%20Code")
    assert response.status_code == 200
    assert b"Results" in response.data
    assert b"No matching records found in the database." not in response.data

def test_camera():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    assert ret is True
    cap.release()

def test_decode_qr_code():
    # Assuming there is a QR code image named "test_qr_code.png" in the project directory
    img = cv2.imread("test_qr_code.png")
    qr_code_data = decode_qr_code(img)
    assert qr_code_data == "Test QR Code"

def test_query_database():
    # Assuming there is a QR code in the database with description "Test QR Code"
    results = query_database("Test QR Code")
    assert len(results) == 1
    assert results[0][0] == "John"
    assert results[0][1] == "Doe"
    assert results[0][2] == "Test Product"
    assert results[0][3] == "2022-04-13"
    assert results[0][4] == "Test QR Code"
    assert results[0][5] is None