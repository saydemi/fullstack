
# app.py - Mock Flask backend (with bugs)
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)

CORS(app) # Enable CORS for all routes


@app.route("/feedback", methods=["GET"])

def get_feedback():
    conn = sqlite3.connect('feedback.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    rating = request.args.get("rating")
    sort = request.args.get("sort", "desc").lower()
    if sort not in ("asc", "desc"):
        sort = "desc"

    # Validate sort direction
    if sort not in ("asc", "desc"):
        sort = "desc"

    query = "SELECT * FROM feedback"
    conditions = []
    params = []

    if rating:
        conditions.append("rating = ?")
        params.append(rating)


    if conditions:
        query += " WHERE " + " AND ".join(conditions)
        query += f" ORDER BY created_at {sort}"

        print("Executing query:", query, "with params:", params)

 
    cursor.execute(query, params)
    feedback = cursor.fetchall()

    feedback = [dict(row) for row in feedback]
    conn.close()
    return jsonify(feedback)


@app.route("/feedback", methods=["POST"])
def post_feedback():
    data = request.get_json()
    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO feedback (message, rating) VALUES (?, ?)", (data["message"], data["rating"]))
    
    

    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})



#ERROR1:missing run statement
if __name__ == '__main__':
    app.run(debug=True)
