"""Auth routes"""

import json
import jsonschema
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import bcrypt, check_password_hash
from jsonschema import validate



auth_bp = Blueprint('auth_bp', __name__)

signup_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "first_name": {
            "type": "string",
            "minLength": 1,
            "trim": True,
            "pattern": "^[A-Za-z\\s]+$"
        },
        "last_name": {
            "type": "string",
            "minLength": 1,
            "trim": True,
            "pattern": "^[A-Za-z\\s]+$"
        },
        "email": {
            "type": "string",
            "format": "email",
        },
        "password": {
            "type": "string",
            "minLength": 6,
            "pattern": "^\\S.*\\S$",
            "trim": True,
        },
        "reason": {
            "type": "string",
            "minLength": 50,
            "trim": True,
        }
    },
    "required": ["first_name", "last_name", "email", "password", "reason"]
}

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login a user"""
    print("got here")
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    with open('users.json', mode="r", encoding="utf") as f:
        data = json.load(f)
    for user in data:
        if user['email'] == email and check_password_hash(user['password'], password):
            if user['status'] == 'pending':
                return jsonify({"msg": "Your application is still being reviewed check back later"}), 401
            access_token = create_access_token(identity=user)
            return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Invalid email or password"}), 401

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """Sign up a new user"""
    try:
        validate(request.json, signup_schema)
        with open('users.json', mode="r", encoding="utf") as f:
            data = json.load(f)
        for user in data:
            if user['email'] == request.json['email']:
                return {'error': 'Email already exists'}, 400
        hashed_password = bcrypt.hashpw(request.json['password'].encode('utf-8'), bcrypt.gensalt())
        print(hashed_password)
        new_user = {
            'first_name': request.json['first_name'],
            'last_name': request.json['last_name'],
            'email': request.json['email'],
            'password': hashed_password.decode('utf-8'),
            'reason': request.json['reason'],
            'id': len(data) + 1,
            "role": "contributor",
            "status": "pending"
        }
        data.append(new_user)
        with open('users.json', 'w', encoding="utf") as f:
            json.dump(data, f)
            del new_user['password']
        return {'success': 'User created', 'user': new_user,
                'token': create_access_token(identity={"id": len(data) + 1,
        "role": "contributor", "email": request.json['email']})}, 201
    except jsonschema.exceptions.ValidationError as exception:
        return {'error': exception.message}, 400
    
@auth_bp.route('/pending-contributors')
@jwt_required()
def get_pending_contributors():
    """ list of pending contributors"""
    user = get_jwt_identity()
    print(user)
    if user.get("status") != "admin":
        return "you are not allowed to do this action", 401
    with open('users.json', mode='r', encoding="utf") as f:
            data = json.load(f)
            print(data)
    return [contributor for contributor in data if contributor.get('status',' None') == 'pending']

@auth_bp.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    """Get a user"""
    token_user = get_jwt_identity()
    print(token_user)
    with open('users.json', mode='r', encoding="utf") as f:
            data = json.load(f)
    for user in data:
        if user.get('id') == token_user.get('id'):
            return user
    return "user not found", 404     
