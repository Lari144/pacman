from flask import Flask, render_template, request
import sqlite3
import qrcode
import io
import base64

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect("qr_codes.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS qr_codes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        qr_code TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.form["data"]
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        qr_code_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")

        conn = sqlite3.connect("qr_codes.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO qr_codes (data, qr_code) VALUES (?, ?)", (data, qr_code_base64))
        conn.commit()
        conn.close()

        return render_template("index.html", qr_code_base64=qr_code_base64)

    return render_template("index.html")

if __name__ == "__main__":
    create_table()
    app.run(debug=True)