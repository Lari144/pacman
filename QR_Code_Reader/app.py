import pyzbar.pyzbar
from QR_Code_Generator import app
from pyzbar.pyzbar import decode
from PIL import Image
import sqlite3
import base64
import io

conn = sqlite3.connect("qr_codes.db")
cursor = conn.cursor()

# Abfrage des QR-Codes aus der Datenbank
cursor.execute("SELECT qr_code FROM qr_codes WHERE qr_id = ?", (qr_id,))
qr_code_base64 = cursor.fetchone()[0]
qr_code_bytes = base64.b64decode(qr_code_base64)
qr_code_image = Image.open(io.BytesIO(qr_code_bytes))

# Dekodieren des QR-Codes
decoded = decode(qr_code_image)
print(decoded[0].data.decode("utf-8"))