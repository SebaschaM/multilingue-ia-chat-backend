# Database
from src.database.db_pg import db
from src.models.requests import Requests


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
                # user_id=data["user_id"],
                user_id=3,  # 3 = Bot
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
