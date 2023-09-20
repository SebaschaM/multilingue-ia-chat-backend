from app import create_app
from sqlalchemy import text

from src.database.db_pg import db

app = create_app()


def execute_sql_file(filename):
    with open(filename, "r") as f:
        init_sql = f.read()

    with db.engine.connect() as connection:
        connection.execute(text(init_sql))
        connection.commit()
        connection.close()


with app.app_context():
    db.create_all()
    execute_sql_file("./init.sql")

if __name__ == "__main__":
    app.run(debug=False, port=5000, host="0.0.0.0")
