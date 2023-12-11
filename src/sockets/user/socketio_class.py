from flask_socketio import join_room, emit, close_room
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

import unicodedata
import base64

from src.services.common.message_service import MessageService
from src.services.common.aws_translate import translate_text


class MessageHandler:
    def __init__(self, socketio_instance):
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        self.private_rooms = {}
        self.socketio = socketio_instance
        self.message_service = MessageService()
        self.clave_codificada = base64.urlsafe_b64encode(self.key).decode("utf-8")
        print(self.clave_codificada, "key codificada")
        print(self.key, "key2")
        

    def encrypt(self, message):
        encrypted_message = self.cipher_suite.encrypt(message.encode())
        return encrypted_message.decode("ascii")

    def decrypt(self, encrypted_message):
        try:
            decrypted_message = self.cipher_suite.decrypt(encrypted_message.encode("ascii"))
            decrypted_message = decrypted_message.decode("utf-8")
            decrypted_message = unicodedata.normalize("NFKD", decrypted_message)
            return decrypted_message
        except InvalidToken as e:
            print(f"Error al descifrar el token: {e}")        


    def send_fernet_key_base_64(self):
        emit(
            "send_fernet_key_base_64",
            {
                "key": self.clave_codificada,
            },
        )

    def assign_user_to_room(self, data):
        room_name = data["room_name"]
        user = data["user"]

        if room_name not in self.private_rooms:
            self.private_rooms[room_name] = [user]
        else:
            if user["fullname"] not in [
                u["fullname"] for u in self.private_rooms[room_name]
            ]:
                if len(self.private_rooms[room_name]) >= 2:
                    emit(
                        "error_joining_room",
                        {
                            "message": "La sala privada ya tiene 2 usuarios asignados. No puedes unirte.",
                            "success": False,
                        },
                    )
                    return
                self.private_rooms[room_name].append(user)

        join_room(room_name)
        self.send_fernet_key_base_64()

        if len(self.private_rooms[room_name]) < 2:
            random_user = self.message_service.get_random_user()
            self.private_rooms[room_name].append(random_user)

        users = self.private_rooms.get(room_name, [])
        # print("USERS: " + str(users))

    def handle_send_message(self, data):
        room_name = data["room_name"]
        fullname = data["fullname"]
        message = data["message"]  # Encriptado
        id_user = data["id"]
        date = data["date"]

        # print("SALAS ACRTUALES: " + str(self.private_rooms))

        # encrypted_message = self.encrypt(message)
        # decrypted_message = self.decrypt(encrypted_message)
        print(message, "RECIBIDO")
        decrypted_message = self.decrypt(message)  # Hacer cambios en el front
        print(decrypted_message)

        users_in_room = self.private_rooms.get(room_name, [])
        users = self.private_rooms.get(room_name, [])

        # Cliente
        user_sender = next((user for user in users if user["id"] == id_user), None)

        # Usuario
        user_receiver = next((user for user in users if user["id"] != id_user), None)
        user_receiver_language = user_receiver["language"]["code_language"]

        # message_translated = translate_text(
        #     message, source="auto", target=str(user_receiver_language)
        # )

        message_translated = translate_text(
            decrypted_message, source="auto", target=str(user_receiver_language)
        )

        encrypted_message_translated = self.encrypt(message_translated)

        if fullname in [u["fullname"] for u in users_in_room]:
            (
                conversation_uuid,
                exist_conversation,
            ) = self.message_service.save_conversation(
                {
                    "user_id": user_receiver["id"],
                    "client_conversation_id": user_sender["id"],
                    "room_name": room_name,
                }
            )
            self.message_service.save_message(
                {
                    "uuid_conversation": conversation_uuid,
                    "id_user_sender": user_sender["id"],
                    "id_user_receiver": user_receiver["id"],
                    # "message_text": message,
                    "message_text": decrypted_message,
                    "message_traslated_text": message_translated,
                    "message_read": 0,
                }
            )
            self.socketio.emit(
                "get_messages",
                data={
                    "room_name": room_name,
                    "fullname": user_sender["fullname"],
                    # "message_text": message,
                    "message_text": message,  # tal cual el front
                    "message_traslated_text": encrypted_message_translated,  # modificacion del backend para la traduccion
                    "id": user_sender["id"],
                    "id_user_sender": user_sender["id"],
                    "id_user_receiver": user_receiver["id"],
                    "date": date,
                    "key": self.key,
                },
                room=room_name,
            )

            if not exist_conversation:
                self.socketio.emit("update_conversations", data={"update": True})

        else:
            emit(
                "error_send_message",
                {
                    "error": "No tienes permiso para enviar mensajes en esta sala privada."
                },
            )

    def handle_close_private_room(self, data):
        room_name = data["room_name"]
        user = data["user"]

        if user["fullname"] in self.private_rooms.get(room_name, []):
            del self.private_rooms[room_name]
            close_room(room_name)
            emit(
                "private_room_closed",
                {
                    "room_name": room_name,
                    "message": f"Sala privada '{room_name}' cerrada por {user['fullname']}.",
                },
            )
        else:
            emit(
                "error", {"message": "No tienes permiso para cerrar esta sala privada."}
            )
