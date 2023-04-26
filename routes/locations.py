#!/usr/bin/python3
"""Locations routes"""
import json

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

locations_bp = Blueprint('locations', __name__)

@locations_bp.route('/locations')
def get_locations():
    """Get all locations"""
    with open('locations.json', mode="r", encoding="utf") as f:
        data = json.load(f)
    return jsonify(data)


@locations_bp.route('/add_locations', methods=['POST'])
def add_location():
    """Add a new location"""
    location = request.get_json()
    with open('locations.json', 'r', encoding="utf") as f:
        data = json.load(f)

    new_location = {
        "name": location["name"],
        "country": location["country"],
        "location": location["location"],
        "img": location["img"],
        "imgs": location["imgs"],
        "description": location["description"],
        "upvotes": [],
        "status": "pending",
        "id": len(data) + 1
    }

    data.append(new_location)

    with open('locations.json', 'w', encoding="utf") as f:
        json.dump(data, f, indent=2)

    return new_location


@locations_bp.route('/pending-locations')
def get_pending_locations():
    """Get all locations that are pending"""
    with open('locations.json', 'r', encoding="utf") as f:
        data = json.load(f)
        print(data)
    return [location for location in data if location.get('status',' None') == 'pending']



@locations_bp.route('/upvote-locations/<int:location_id>', methods=['PATCH'])
@jwt_required()
def put_upvote_pending_locations_id(location_id):
    """Upvote or agree to locations that are pending"""
    user = get_jwt_identity()
    with open('locations.json', 'r', encoding="utf") as f:
        data = json.load(f)
    for location in data:
        print(location.get("id"), location_id, user.get("id"))  
        try:
            if location['id'] == int(location_id) and location.get("status", None) == "pending":
                if 'upvotes' not in location:
                    location['upvotes'] = []
                if user.get("id") not in location['upvotes']:
                    location['upvotes'].append(user.get("id"))
                else:
                    return 'You have already upvoted this location', 400
        except ValueError:
            return 'Invalid location id', 400
    with open('locations.json', 'w', encoding="utf") as f:
        json.dump(data , f, indent=2)
        return 'Location upvoted successfully. Thank you for your input!'
