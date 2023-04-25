#!/usr/bin/python3
"""Locations routes"""
import json

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

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
    with open('locations.json') as f:
        data = json.load(f)

    new_location = {
        "name": location["name"],
        "country": location["country"],
        "location": location["location"],
        "img": location["img"],
        "imgs": location["imgs"],
        "description": location["description"],
        "approval": [],
        "status": "pending"
    }

    data.append(new_location)

    with open('locations.json', 'w') as f:
        json.dump(data, f, indent=2)

    return new_location


@locations_bp.route('/pending-locations')
def get_pending_locations():
    """Get all locations that are pending"""
    with open('locations.json', 'r') as f:
        data = json.load(f)
        print(data)
    return [location for location in data if location.get('status',' None') == 'pending']



@locations_bp.route('/upvote-locations', methods=['PUT'])
def put_upvote_pending_locations_id():
    """Upvote or agree to locations that are pending"""
    with open('locations.json', 'r') as f:
        data = json.load(f)
        print(data)


    for location in data ['locations']:
        if location ['id'] == 'location_id' and location ['status'] == 'pending':
            if 'upvotes' not in location:
                location ['upvotes'] = []

    location['upvotes'].append(request.form['contributor_id'])
    with open('locations.json', 'w') as f:
        json.dump(data , f, indent=2)
        if 'upvotes' == True:

          return 'Location upvoted successfully. Thank you for your input!'

        else:

          return 'Location not found or nor pending. Check back later!'
