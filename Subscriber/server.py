# Code for the subscriber to receive the sensor data and make predictions

import json
import os
import sqlite3

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def get_db_connection(dir="db/database.db"):
    conn = sqlite3.connect(dir)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/falls", methods=["GET"])
def get_falls():
    conn = get_db_connection()
    falls = conn.execute("SELECT * FROM Accidents").fetchall()
    conn.close()
    return json.dumps([dict(i) for i in falls])


port = int(os.environ.get("PORT", 5000))
app.run(debug=True, host="0.0.0.0", port=port)
