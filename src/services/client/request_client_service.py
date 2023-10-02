# Database
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid

from src.database.db_pg import db
from src.models.requests import Requests
from src.utils.security import Security


class RequestClientService:
    @classmethod
    def register_request(cls, data):
        try:
            request = Requests(
                date_attention=data["date_attention"],
                reason=data["reason"],
                destination_area=data["destination_area"],
                request_type_id=2,
                status_id=2,
                user_id=data["user_id"],
                client_id=data["client_id"],
            )

            db.session.add(request)
            db.session.commit()

            return {
                "message": "Request created successfully",
                "success": True,
            }, 201
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500

    @classmethod
    def get_requests(cls):
        try:
            requests = Requests.query.all()
            requests = [request.to_dict() for request in requests]
            return {"requests": requests}, 200
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500
