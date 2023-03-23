from flask import Flask, render_template, request
import sqlite3
import qrcode
import io
import base64

class QRCodeGenerator:
    def __init__(self):
        self.conn = sqlite3.connect("qr_codes.db")
        self.cursor = self.conn.cursor()

    def create_qr_code(self, qr_description, product_id):
        self.cursor.execute("INSERT INTO qr_codes (product_id, description, qr_code) VALUES (?, ?, ?)",
                    (product_id, qr_description, ''))

        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(qr_description)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        qr_code_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")

        self.qr_code_base64 = qr_code_base64

        self.cursor.execute("UPDATE qr_codes SET qr_code = ? WHERE product_id = ?", (qr_code_base64, product_id))

        self.conn.commit()
    
    def __del__(self):
        self.conn.close()

class QRCodeReader:
    def __init__(self):
        self.conn = sqlite3.connect("qr_codes.db")
        self.cursor = self.conn.cursor()

    def read_qr_code(self, qr_code_base64):
        self.cursor.execute("SELECT description FROM qr_codes WHERE qr_code = ?", (qr_code_base64,))
        row = self.cursor.fetchone()
        if row is None:
            return None
        else:
            return row[0]
    
    def __del__(self):
        self.conn.close()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        address = request.form["address"]
        order_date = request.form["order_date"]
        product_description = request.form["product_description"]
        qr_description = request.form["qr_description"]
        location_description = request.form["location_description"]

        conn = sqlite3.connect("qr_codes.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO customers (First_Name, Last_Name, Address) VALUES (?, ?, ?)",
                       (first_name, last_name, address))
        customer_id = cursor.lastrowid

        cursor.execute("INSERT INTO products (customer_id, order_date, description) VALUES (?, ?, ?)",
                        (customer_id, order_date, product_description))
        product_id = cursor.lastrowid

        qr_generator = QRCodeGenerator()
        qr_generator.create_qr_code(qr_description, product_id)  
        qr_code_base64 = qr_generator.qr_code_base64

        cursor.execute("INSERT INTO locations (product_id, description) VALUES (?, ?)",
                        (product_id, location_description))

        conn.commit()
        conn.close()

        return render_template("index.html", qr_code_base64=qr_code_base64)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)