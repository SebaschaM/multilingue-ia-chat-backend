# Database
from datetime import datetime

from src.database.db_pg import db
from src.models.notifications import Notifications


class NotificationAdminService:
    @classmethod
    def register_notification(cls, data):
        try:
            message = data["message"]
            start_time = data["start_date"]
            end_time = data["end_date"]

            notification = Notifications(
                message=message,
                start_time=start_time,
                end_time=end_time,
                state="active",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

            db.session.add(notification)
            db.session.commit()

            return {
                "message": "Notificación registrada correctamente.",
                "success": True,
            }, 201

        except Exception as e:
            return {
                "error": str(e),
                "success": False,
            }, 500

    @classmethod
    def get_notifications(cls):
        try:
            notifications = Notifications.query.all()

            if notifications is None:
                return {
                    "message": "No hay notificaciones registradas.",
                    "success": True,
                    "data": {},
                }, 200

            return {
                "message": "Notificaciones registradas.",
                "success": True,
                "data": [notification.to_dict() for notification in notifications],
            }, 200

        except Exception as e:
            return {
                "error": str(e),
                "success": False,
            }, 500

    @classmethod
    def get_notifications_active(cls):
        try:
            notifications = Notifications.query.filter_by(state="active").all()

            if notifications is None:
                return {
                    "message": "No hay notificaciones activas.",
                    "success": True,
                    "data": {},
                }, 200

            return {
                "message": "Notificaciones activas.",
                "success": True,
                "data": [notification.to_dict() for notification in notifications],
            }, 200

        except Exception as e:
            return {
                "error": str(e),
                "success": False,
            }, 500

    @classmethod
    def update_notifications_active(cls, id, data):
        try:
            notification = Notifications.query.filter_by(id=id).first()

            if notification is None:
                return {
                    "message": "No se encontró la notificación.",
                    "success": True,
                    "data": {},
                }, 200

            notification.message = data["message"]
            notification.start_time = data["start_time"]
            notification.end_time = data["end_time"]
            notification.state = data["state"]
            notification.updated_at = datetime.now()

            db.session.commit()

            return {
                "message": "Notificación actualizada correctamente.",
                "success": True,
            }, 201

        except Exception as e:
            return {
                "error": str(e),
                "success": False,
            }, 500

    @classmethod
    def delete_notifications_active(cls, id):
        try:
            notification = Notifications.query.filter_by(id=id).first()

            if notification is None:
                return {
                    "message": "No se encontró la notificación.",
                    "success": True,
                    "data": {},
                }, 200

            db.session.delete(notification)
            db.session.commit()

            return {
                "message": "Notificación eliminada correctamente.",
                "success": True,
            }, 201

        except Exception as e:
            return {
                "error": str(e),
                "success": False,
            }, 500
