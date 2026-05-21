from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# ================= DATABASE =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "pos.db")


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# ================= CUSTOMERS =================
@app.route("/customers")
def customers():
    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM customers")
        rows = cur.fetchall()

        conn.close()
        return jsonify([dict(row) for row in rows])

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================= INVENTORY =================
@app.route("/inventory")
def inventory():
    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM inventory")
        rows = cur.fetchall()

        conn.close()
        return jsonify([dict(row) for row in rows])

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================= SALES =================
@app.route("/sales")
def sales():
    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM sales")
        rows = cur.fetchall()

        conn.close()
        return jsonify([dict(row) for row in rows])

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================= HOME =================
@app.route("/")
def home():
    return jsonify({
        "status": "API Running",
        "message": "POS API working"
    })


# ================= RUN (RENDER SAFE) =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)