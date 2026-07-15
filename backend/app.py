"""
app.py
------
Backend for SaveWise (spare-change round-up savings app).
"Save Smarter. Spend Wiser."

Built with Flask + SQLite. No login/auth — this stores data for
a single user, which is enough for a demo/project.

Run it with:
    pip install -r requirements.txt
    python app.py

Then open http://127.0.0.1:5000 in your browser.
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import math
import os

app = Flask(__name__, static_folder="static")
CORS(app)  # allows the frontend to call this API even if opened from a different origin

DB_FILE = os.path.join(os.path.dirname(__file__), "savewise.db")


# =========================================================
# DATABASE SETUP
# =========================================================
def get_db():
    """Open a connection to the SQLite database file."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # lets us access columns by name, e.g. row["amount"]
    return conn


def init_db():
    """Create the tables if they don't exist yet. Runs once on startup."""
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            roundup REAL NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS goal (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            target REAL NOT NULL
        )
    """)
    # Make sure a single goal row always exists (default target ₹1000)
    conn.execute("INSERT OR IGNORE INTO goal (id, target) VALUES (1, 1000)")
    conn.commit()
    conn.close()


# =========================================================
# HELPER: round-up calculation
# Rounds a spend amount up to the nearest ₹10 and returns
# how much of that is "saved" (the round-up amount).
# =========================================================
def compute_roundup(amount):
    rounded = math.ceil(amount / 10) * 10
    return round(rounded - amount, 2)


# =========================================================
# ROUTE: serve the frontend
# =========================================================
@app.route("/")
def serve_frontend():
    return send_from_directory(app.static_folder, "index.html")


# =========================================================
# ROUTE: GET  /api/transactions  -> list all transactions
# ROUTE: POST /api/transactions  -> add a new transaction
# =========================================================
@app.route("/api/transactions", methods=["GET", "POST"])
def transactions():
    conn = get_db()

    if request.method == "GET":
        rows = conn.execute(
            "SELECT * FROM transactions ORDER BY id DESC"
        ).fetchall()
        conn.close()
        return jsonify([dict(row) for row in rows])

    # POST: add a new transaction
    data = request.get_json()
    description = data.get("description", "Untitled expense")
    amount = float(data.get("amount", 0))
    category = data.get("category", "Other")

    if amount <= 0:
        conn.close()
        return jsonify({"error": "Amount must be greater than 0"}), 400

    roundup = compute_roundup(amount)

    cursor = conn.execute(
        "INSERT INTO transactions (description, amount, category, roundup) VALUES (?, ?, ?, ?)",
        (description, amount, category, roundup)
    )
    conn.commit()

    new_row = conn.execute(
        "SELECT * FROM transactions WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    conn.close()

    return jsonify(dict(new_row)), 201


# =========================================================
# ROUTE: GET /api/summary -> totals for the dashboard
# =========================================================
@app.route("/api/summary", methods=["GET"])
def summary():
    conn = get_db()
    row = conn.execute("""
        SELECT
            COALESCE(SUM(amount), 0)  AS total_spent,
            COALESCE(SUM(roundup), 0) AS total_saved,
            COUNT(*)                  AS count
        FROM transactions
    """).fetchone()
    conn.close()
    return jsonify(dict(row))


# =========================================================
# ROUTE: GET /api/analytics -> spending grouped by category
# =========================================================
@app.route("/api/analytics", methods=["GET"])
def analytics():
    conn = get_db()
    rows = conn.execute("""
        SELECT category, SUM(amount) AS total
        FROM transactions
        GROUP BY category
        ORDER BY total DESC
    """).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])


# =========================================================
# ROUTE: GET  /api/goal -> current savings goal
# ROUTE: POST /api/goal -> update the savings goal
# =========================================================
@app.route("/api/goal", methods=["GET", "POST"])
def goal():
    conn = get_db()

    if request.method == "GET":
        row = conn.execute("SELECT target FROM goal WHERE id = 1").fetchone()
        conn.close()
        return jsonify(dict(row))

    # POST: update the goal target
    data = request.get_json()
    target = float(data.get("target", 1000))
    conn.execute("UPDATE goal SET target = ? WHERE id = 1", (target,))
    conn.commit()
    conn.close()
    return jsonify({"target": target})


# =========================================================
# ROUTE: DELETE /api/transactions/<id> -> remove one transaction
# (Recalculates totals automatically since summary/analytics
#  are computed live from the transactions table.)
# =========================================================
@app.route("/api/transactions/<int:tx_id>", methods=["DELETE"])
def delete_transaction(tx_id):
    conn = get_db()
    conn.execute("DELETE FROM transactions WHERE id = ?", (tx_id,))
    conn.commit()
    conn.close()
    return jsonify({"deleted": tx_id})


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
