from app import create_app
from sqlalchemy import text

from src.database.db_pg import db
from src.models.seeds import create_seed

app = create_app()

with app.app_context():
    db.create_all()
    create_seed()

if __name__ == "__main__":
    app.run(debug=False, port=5000, host="0.0.0.0")
