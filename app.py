#!/usr/bin/python3
"""This module defines a Flask application that serves a RESTful API"""

from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/locations')
def get_locations():
    with open('locations.json') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
