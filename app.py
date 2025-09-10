import os
import sqlite3
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for  # ← добавили request, redirect, url_for

APP_NAME = "Budget Tracker (Step-by-step)"
DB_NAME = "budget.db"

app = Flask(__name__, instance_relative_config=True)
DB_PATH = os.path.join(app.instance_path, DB_NAME)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tx_date TEXT NOT NULL,           -- YYYY-MM-DD
            kind TEXT CHECK(kind IN ('income','expense')) NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL CHECK(amount >= 0),
            note TEXT
        );
        """
    )
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = get_db()
    rows = conn.execute(
        "SELECT id, tx_date, kind, category, amount, note FROM transactions ORDER BY tx_date DESC, id DESC"
    ).fetchall()
    conn.close()
    return render_template("index.html", app_name=APP_NAME, txs=rows)

@app.route("/add", methods=["POST"])
def add():
    # 1) забираем значения из формы
    tx_date = (request.form.get("tx_date") or "").strip()
    kind = request.form.get("kind")
    category = (request.form.get("category") or "").strip() or "General"
    amount_raw = request.form.get("amount")
    note = (request.form.get("note") or "").strip()

    # 2) простая валидация
    if kind not in ("income", "expense"):
        return "Invalid kind", 400
    try:
        amount = round(float(amount_raw), 2)
        if amount < 0:
            raise ValueError
    except (TypeError, ValueError):
        return "Amount must be a non-negative number", 400
    if not tx_date:
        return "Date is required (YYYY-MM-DD)", 400

    # 3) запись в БД
    conn = get_db()
    conn.execute(
        "INSERT INTO transactions (tx_date, kind, category, amount, note) VALUES (?, ?, ?, ?, ?)",
        (tx_date, kind, category, amount, note),
    )
    conn.commit()
    conn.close()

    # 4) редирект на список
    return redirect(url_for("index"))

if __name__ == "__main__":
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    init_db()
    app.run(debug=True)
