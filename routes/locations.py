#!/usr/bin/python3
"""Locations routes"""
import json

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

locations_bp = Blueprint('locations', __name__)

@locations_bp.route('/locations')
def get_locations():
    """Get all locations"""
    with open('locations.json', mode="r", encoding="utf") as f:
        data = json.load(f)
    return jsonify(data)
