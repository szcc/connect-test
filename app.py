# app.py
import os
from flask import Flask, jsonify

# This *must* be named "app"
app = Flask(__name__)


@app.get("/")
def index():
    return jsonify(
        #REQUESTS_CA_BUNDLE=os.environ.get("REQUESTS_CA_BUNDLE")
        "REQUESTS_CA_BUNDLE": os.environ.get("REQUESTS_CA_BUNDLE"),
        "sqlite_db_exists": os.path.exists(DB_PATH),
    )

@app.get("/write")
def write():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO demo (value) VALUES (?)", ("Hello from Connect",))
    conn.commit()
    conn.close()
    return {"status": "write ok"}

@app.get("/read")
def read():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    rows = c.execute("SELECT * FROM demo").fetchall()
    conn.close()
    return {"rows": rows}
