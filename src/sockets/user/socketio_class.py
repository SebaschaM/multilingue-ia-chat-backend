from flask import Blueprint
from flask_socketio import join_room, emit, close_room
from cryptography.fernet import Fernet
import unicodedata


class MessageHandler:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        self.private_rooms = {}

    def encrypt(self, message):
        encrypted_message = self.cipher_suite.encrypt(message.encode())
        return encrypted_message.decode("ascii")

    def decrypt(self, encrypted_message):
        decrypted_message = self.cipher_suite.decrypt(encrypted_message.encode("ascii"))
        decrypted_message = decrypted_message.decode("utf-8")
        decrypted_message = unicodedata.normalize("NFKD", decrypted_message)
        return decrypted_message

    def assign_user_to_room(self, data):
        room_name = data["room_name"]
        username = data["username"]
        print(f"Usuario {username} asignado a la sala {room_name}")

        if room_name not in self.private_rooms:
            self.private_rooms[room_name] = [username]
            join_room(room_name)

        elif username not in self.private_rooms[room_name]:
            if len(self.private_rooms[room_name]) >= 2:
                emit(
                    "error",
                    {
                        "message": "La sala privada ya tiene 2 usuarios asignados. No puedes unirte.",
                        "success": False,
                    },
                )
            else:
                self.private_rooms[room_name].append(username)
                join_room(room_name)

        print(
            f"Los usuarios en la sala {room_name} son: {self.private_rooms.get(room_name, [])}"
        )

    def handle_send_message(self, data):
        room_name = data["room_name"]
        username = data["username"]
        message = data["message"]

        print(f"Mensaje recibido: {message}")
        encrypted_message = self.encrypt(message)
        print(" mensaje encriptado", encrypted_message)
        decrypted_message = self.decrypt(encrypted_message)
        print(" mensaje desencriptado", decrypted_message)

        # Obtén la lista de usuarios en la sala
        users_in_room = self.private_rooms.get(room_name, [])

        if username in users_in_room:
            # Enviar el mensaje a todos los usuarios en la sala excepto al usuario actual
            for user in users_in_room:
                if user != username:
                    emit(
                        "message",
                        {
                            "room_name": room_name,
                            "username": username,
                            "message": message,
                        },
                        room=room_name,
                    )
        else:
            emit(
                "error",
                {
                    "message": "No tienes permiso para enviar mensajes en esta sala privada."
                },
            )

    def handle_close_private_room(self, data):
        room_name = data["room_name"]
        username = data["username"]

        if username in self.private_rooms.get(room_name, []):
            del self.private_rooms[room_name]
            close_room(room_name)
            emit(
                "private_room_closed",
                {
                    "room_name": room_name,
                    "message": f"Sala privada '{room_name}' cerrada por {username}.",
                },
            )
        else:
            emit(
                "error", {"message": "No tienes permiso para cerrar this sala privada."}
            )
