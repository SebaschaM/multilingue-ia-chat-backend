# Database
from src.database.db_pg import db
from src.models.requests import Requests


class RequestAdminService:
    @classmethod
    def register_request(cls, data):
        try:
            request = Requests(
                date_attention=data["date_attention"],
                reason=data["reason"],
                destination_area=data["destination_area"],
                request_type_id=2,  # 1: Typification, 2: Scheduling
                status_id=2,
                user_id=data["user_id"],
                client_id=data["client_id"],
            )

            db.session.add(request)
            db.session.commit()

            return {
                "message": "Se creo la solicitud exitosamente",
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

    @classmethod
    def get_request_by_id(cls, id):
        try:
            request = Requests.query.get(id)
            request = request.to_dict()
            return {"request": request}, 200
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500

    @classmethod
    def change_state_request(cls, data):
        try:
            request_id = data["request_id"]
            status_id = data["status_id"]

            request = Requests.query.get(request_id)
            request.status_id = status_id

            db.session.commit()

            return {
                "message": "Se actualizo el estado de la solicitud exitosamente",
                "success": True,
            }, 200
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500

    @classmethod
    def delete_request(cls, id):
        try:
            request = Requests.query.get(id)
            db.session.delete(request)
            db.session.commit()
            return {"message": "Se elimino la solicitud correctamente"}, 200
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500
