from flask import Blueprint, request, jsonify
import logging

from src.services.auth_service import AuthService
from src.middleware.token_required import token_required
from flask_socketio import SocketIO


message_bp = Blueprint("message", __name__)
logging.basicConfig(level=logging.DEBUG)
socketio = SocketIO()



@message_bp.route("/message", methods=["POST"])
def send_message():
    message = request.json.get("message")
    print("Sent message:", message)
    response_data = {"message": "Mensaje enviado correctamente"}
    return jsonify(response_data), 200

@socketio.on('connect')
def handle_connect():
    print("Connected desde la carpeta sockets")


    logging.info('Cliente conectado')
    socketio.emit('connected', {'data': 'Connected'})

@socketio.on('message')
def handle_message(data):
    message = request.json.get("message")
    print("Sent message:", message)

    print(data)

   