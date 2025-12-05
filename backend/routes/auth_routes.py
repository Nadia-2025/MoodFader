from flask import Blueprint, request, jsonify
from database import db
from models.users import User
import jwt
import os
from datetime import datetime, timedelta

auth_bp = Blueprint("auth_bp", __name__)
SECRET_KEY = os.getenv("SECRET_KEY")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    
    # Validar campos requeridos
    required_fields = ["email", "username", "password"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    
    # Validar que el email no exista
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400
    
    # Validar que el username no exista
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already taken"}), 400
    
    # Crear nuevo usuario
    new_user = User(email=email, username=username)
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    
    # Validar campos
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    
    # Buscar usuario
    user = User.query.filter_by(email=email).first()
    
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401
    
    # Generar JWT
    token = jwt.encode(
        {
            "user_id": user.id,
            "email": user.email,
            "username": user.username,
            "exp": datetime.utcnow() + timedelta(hours=24)
        },
        SECRET_KEY,
        algorithm="HS256"
    )
    
    return jsonify({
        "message": "Login successful",
        "access_token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username
        }
    }), 200

@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    token = request.headers.get("Authorization")
    
    if not token:
        return jsonify({"error": "Missing token"}), 401
    
    try:
        # Extraer el token del header "Bearer <token>"
        payload = jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=["HS256"])
        user_id = payload["user_id"]
    except Exception as e:
        return jsonify({"error": "Invalid token"}), 401
    
    # Buscar usuario
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Generar nuevo token
    new_token = jwt.encode(
        {
            "user_id": user.id,
            "email": user.email,
            "username": user.username,
            "exp": datetime.utcnow() + timedelta(hours=24)
        },
        SECRET_KEY,
        algorithm="HS256"
    )
    
    return jsonify({
        "message": "Token refreshed",
        "access_token": new_token
    }), 200
