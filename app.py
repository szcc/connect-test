# app.py
import os
import sqlite3
import ssl
import requests
from flask import Flask, jsonify

# This *must* be named "app"
app = Flask(__name__)
DB_PATH = os.path.join(os.getcwd(), "test.db")

@app.get("/")
def index():
    return jsonify(
        REQUESTS_CA_BUNDLE=os.environ.get("REQUESTS_CA_BUNDLE"),
        
        SQLITE_DB_EXISTS=os.path.exists(DB_PATH),
        DB_PATH=DB_PATH,
        
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

@app.get("/openssl")
def openssl_info():
    info = {
        "PYTHON_OPENSSL": ssl.OPENSSL_VERSION,
        "REQUESTS_CA_BUNDLE": os.environ.get("REQUESTS_CA_BUNDLE"),
    }

    # Test external HTTPS
    try:
        r = requests.get("https://www.google.com", timeout=5)
        info["google_status"] = r.status_code
    except Exception as e:
        info["google_error"] = str(e)

    # Test internal HTTPS
    url = "https://langfuse.toxpipe.niehs.nih.gov/api/public/otel/v1/traces"
    try:
        r2 = requests.get(url, timeout=5)
        info["langfuse_status"] = r2.status_code
    except Exception as e:
        info["langfuse_error"] = str(e)

    return jsonify(info)
