import sqlite3
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)
DB_NAME = "campus_tracker.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grievances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            category TEXT NOT NULL,
            location TEXT NOT NULL,
            description TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/grievances", methods=["GET"])
def get_grievances():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM grievances ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route("/api/grievances", methods=["POST"])
def add_grievance():
    data = request.json
    student_name = data.get("student_name")
    category = data.get("category")
    location = data.get("location")
    description = data.get("description")
    priority = data.get("priority", "Medium")
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    if not all([student_name, category, location, description]):
        return jsonify({"error": "Missing required fields"}), 400

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO grievances (student_name, category, location, description, priority, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (student_name, category, location, description, priority, created_at))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({"message": "Grievance lodged successfully", "ticket_id": new_id}), 201

@app.route("/api/grievances/<int:ticket_id>/status", methods=["PATCH"])
def update_status(ticket_id):
    data = request.json
    new_status = data.get("status")
    
    if new_status not in ["Pending", "In Progress", "Resolved"]:
        return jsonify({"error": "Invalid status"}), 400

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE grievances SET status = ? WHERE id = ?", (new_status, ticket_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Status updated successfully"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)