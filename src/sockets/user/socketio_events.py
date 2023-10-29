from flask_socketio import SocketIO
from .socketio_class import MessageHandler

socketio = SocketIO(cors_allowed_origins="*")
message_handler = MessageHandler(socketio_instance=socketio)


@socketio.on("assign_user_to_room")
def handle_assign_user_to_room(data):
    message_handler.assign_user_to_room(data)


@socketio.on("send_message")
def handle_send_message(data):
    message_handler.handle_send_message(data)


@socketio.on("close_room")
def handle_close_room(data):
    message_handler.handle_close_private_room(data)
