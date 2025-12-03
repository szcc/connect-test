# app.py
import os
from flask import Flask, jsonify

# This *must* be named "app"
app = Flask(__name__)


@app.get("/")
def index():
    return jsonify(
        REQUESTS_CA_BUNDLE=os.environ.get("REQUESTS_CA_BUNDLE")
    )

