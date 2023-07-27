from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Configuration for SQLite database
DB_NAME = "inventory.db"

# Create the SQLite database and table if they don't exist
def create_tables():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id TEXT PRIMARY KEY,
                product_name TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS locations (
                location_id TEXT PRIMARY KEY,
                location_name TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_movements (
                movement_id TEXT PRIMARY KEY,
                timestamp TEXT,
                from_location TEXT,
                to_location TEXT,
                product_id TEXT,
                qty INTEGER,
                FOREIGN KEY (from_location) REFERENCES locations(location_id),
                FOREIGN KEY (to_location) REFERENCES locations(location_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        """)
        conn.commit()

create_tables()

# Helper function to get the current timestamp
def get_current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@app.route("/")
def index():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM product_movements ORDER BY timestamp DESC")
        movements = cursor.fetchall()
    return render_template("index.html", movements=movements)

@app.route("/add_movement", methods=["POST"])
def add_movement():
    movement_id = request.form["movement_id"]
    from_location = request.form["from_location"]
    to_location = request.form["to_location"]
    product_id = request.form["product_id"]
    qty = request.form["qty"]
    timestamp = get_current_timestamp()

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO product_movements (movement_id, timestamp, from_location, to_location, product_id, qty) VALUES (?, ?, ?, ?, ?, ?)",
                       (movement_id, timestamp, from_location, to_location, product_id, qty))
        conn.commit()

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
