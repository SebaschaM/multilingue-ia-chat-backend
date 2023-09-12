from src.database.db_pg import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    date_of_birth = db.Column(db.Date)
    cellphone = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(
        self,
        email,
        password,
        name,
        lastname,
        date_of_birth,
        cellphone,
    ):
        self.email = email
        self.password = password
        self.name = name
        self.lastname = lastname
        self.date_of_birth = date_of_birth
        self.cellphone = cellphone

    def to_dict(self):
        return {
            "email": self.email,
            "name": self.name,
            "lastname": self.lastname,
            "date_of_birth": self.date_of_birth,
            "cellphone": self.cellphone,
        }
