from app import db


class CustomUser(db.Model):
    __tablename__ = "CustomUser"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)

    last_name = db.Column(db.String(50), nullable=False)

    email = db.Column(db.String(150))

    def __init__(self, first_name, last_name, email=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __repr__(self):
        return f"<CustomUser id {self.id}"
