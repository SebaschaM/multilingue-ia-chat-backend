from flask import Blueprint, request, jsonify
from src.models.user import User
from src.services.auth_service import AuthService
from src.database.db_pg import db


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/sigin", methods=["POST"])
def sigin():
    # Obtiene los datos del usuario desde el body del request
    username = request.json.get("username")
    password = request.json.get("password")

    # Si el usuario o la contraseña no existen, devuelve un error
    if not username or not password:
        return jsonify({"error": "Usuario y contraseña requeridos"}), 400

    # Registra al usuario
    response, status = AuthService.login_user(username, password)

    # Devuelve la respuesta y el código de estado HTTP
    return jsonify(response), status


@auth_bp.route("/sigup", methods=["POST"])
def sigup():
    # Obtiene los datos del usuario desde el body del request
    username = request.json.get("username")
    password = request.json.get("password")

    # Si el usuario o la contraseña no existen, devuelve un error
    if not username or not password:
        return jsonify({"error": "Usuario y contraseña requeridos"}), 400

    # Registra al usuario
    response, status = AuthService.register_user(username, password)

    # Devuelve la respuesta y el código de estado HTTP
    return jsonify(response), status
