# PARA LA TAREA
from sqlalchemy import text
from datetime import datetime, timedelta


class Schedules:
    @classmethod
    def block_users(cls, app, db):
        with app.app_context():
            current_date = datetime.now()
            limit_date = current_date - timedelta(days=10)
            query = text(
                "SELECT id, blocked FROM users WHERE last_login <= :limit_date"
            )
            response = db.session.execute(query, {"limit_date": limit_date})

            if response.rowcount == 0:
                return

            for row in response:
                user_id, blocked = row
                if blocked == 0:
                    update_query = text(
                        "UPDATE users SET blocked = 1 WHERE id = :user_id"
                    )
                    db.session.execute(update_query, {"user_id": user_id})

            db.session.commit()
