from flask import Blueprint

# from src.services.auth_service import AuthService
from src.middleware.token_required import token_required
from app import socketio
from flask_socketio import join_room, rooms, emit, close_room
from hashlib import md5
from cryptography.fernet import Fernet
import unicodedata

message_bp = Blueprint("message", __name__)

# TODO: Generar una clave para cifrar y descifrar
key = Fernet.generate_key()
cipher_suite = Fernet(key)


def encrypt(message):
    encrypted_message = cipher_suite.encrypt(message.encode())
    return encrypted_message.decode("ascii")


def decrypt(encrypted_message):
    decrypted_message = cipher_suite.decrypt(encrypted_message.encode("ascii"))

    # Decodificar el mensaje a Unicode
    decrypted_message = decrypted_message.decode("utf-8")

    # Normalizar el mensaje
    decrypted_message = unicodedata.normalize("NFKD", decrypted_message)

    return decrypted_message


# EVENTOS DEL SOCKET IO
private_rooms = {}


@socketio.on("connect")
def handle_connect():
    print("Connect")


@socketio.on("login")
def handle_login(data):
    username = data["username"]
    print(username)

    emit("login_response", {"message": f"Bienvenido, {username}!"})


@socketio.on("creacion_de_sala_privada")
def handle_create_private_room(data):
    room_name = data["room_name"]
    username = data["username"]
    print(data)

    if room_name not in private_rooms:
        private_rooms[room_name] = [username]
        join_room(room_name)
        # print("private_rooms1", private_rooms)
        emit(
            "private_room_created",
            {
                "room_name": room_name,
                "message": f"Sala privada '{room_name}' creada con éxito.",
            },
        )
    else:
        # Verifica si el usuario ya está en la sala
        if username not in private_rooms.get(room_name, []):
            private_rooms[room_name].append(username)
            join_room(room_name)
            private_rooms[room_name] = list(set(private_rooms[room_name]))

            print("private_rooms2", private_rooms)
            emit(
                "private_room_created",
                {
                    "room_name": room_name,
                    "message": f"Sala privada '{room_name}' anteriormente creada con éxito.",
                },
            )
        else:
            # print(f"Usuario '{username}' ya está en la sala '{room_name}'. No se agregará nuevamente.")
            # Eliminar duplicados si existen
            private_rooms[room_name] = list(set(private_rooms[room_name]))
            # print("private_rooms después de eliminar duplicados", private_rooms)


@socketio.on("asociacion_de_usuarios_a_la_sala_privada")
def handle_join_private_room(data):
    room_name = data["room_name"]
    username = data["username"]

    if room_name in private_rooms:
        # private_rooms[room_name].append(username)
        join_room(room_name)

        emit(
            "user_joined_private_room",
            {
                "room_name": room_name,
                "username": username,
                "message": f"{username} se unió a la sala privada.",
            },
            room=room_name,
        )
    else:
        emit("error", {"message": f"La sala privada '{room_name}' no existe."})


# CREAR OTRO EVENTO DE VALIDACIÓN DE LOS PRIVATE ROOM, SI YA EXISTEN 2 USUARIOS EN LA SALA, NO DEJAR ENTRAR A MÁS USUARIOS Y QUE CREE OTRO ROOM
# POR DEFECTO QUE ASIGNE AL CHATBOT A LA SALA PRIVADA Y AL CLIENTE


@socketio.on("envio_de_mensajes")
def handle_send_message(data):
    room_name = data["room_name"]
    username = data["username"]
    message = data["message"]

    print(f"Mensaje recibido: {message}")
    # Encriptar el mensaje
    encrypted_message = encrypt(message)
    print(" mensaje encriptado", encrypted_message)

    # Desencriptar el mensaje
    decrypted_message = decrypt(encrypted_message)

    print(" mensaje desencriptado", decrypted_message)

    if username in private_rooms.get(room_name, []):
        # print(" debug", username, private_rooms, room_name)
        emit(
            "message",
            {"room_name": room_name, "username": username, "message": message},
            room=room_name,
        )
    else:
        emit(
            "error",
            {"message": "No tienes permiso para enviar mensajes en esta sala privada."},
        )


@socketio.on("cierre_de_la_sala_privada")
def handle_close_private_room(data):
    room_name = data["room_name"]
    username = data["username"]

    if username in private_rooms.get(room_name, []):
        del private_rooms[room_name]
        close_room(room_name)
        emit(
            "private_room_closed",
            {
                "room_name": room_name,
                "message": f"Sala privada '{room_name}' cerrada por {username}.",
            },
        )
    else:
        emit("error", {"message": "No tienes permiso para cerrar esta sala privada."})
