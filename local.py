from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)

# ================= DATABASE =================
DATABASE_URL = os.environ.get("DATABASE_URL")

# Fix Railway PostgreSQL issue
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ================= MODELS =================

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)


class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    total = db.Column(db.Float)


# ================= CREATE TABLES =================
with app.app_context():
    db.create_all()


# ================= ROUTES =================

@app.route("/customers")
def customers():
    rows = Customer.query.all()
    return jsonify([{"id": r.id, "name": r.name, "phone": r.phone} for r in rows])


@app.route("/inventory")
def inventory():
    rows = Inventory.query.all()
    return jsonify([{
        "id": r.id,
        "name": r.name,
        "price": r.price,
        "stock": r.stock
    } for r in rows])


@app.route("/sales")
def sales():
    rows = Sales.query.all()
    return jsonify([{
        "id": r.id,
        "product_name": r.product_name,
        "quantity": r.quantity,
        "total": r.total
    } for r in rows])


@app.route("/")
def home():
    return jsonify({
        "status": "API Running",
        "message": "POS API with PostgreSQL working"
    })


# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
