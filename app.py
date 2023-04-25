#!/usr/bin/python3
"""This module defines a Flask application that serves a RESTful API"""
from flask_jwt_extended import JWTManager
from flask import Flask
from flask_cors import CORS
from routes.auth import auth_bp
from routes.locations import locations_bp



app = Flask(__name__)
CORS(app)
app.register_blueprint(auth_bp)
app.register_blueprint(locations_bp)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
