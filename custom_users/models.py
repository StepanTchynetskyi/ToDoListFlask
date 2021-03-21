from app import db
from sqlalchemy.exc import IntegrityError

class CustomUser(db.Model):
    __tablename__ = "CustomUser"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(50), nullable=False)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<CustomUser id {self.id}"

    def to_dict(self):
        return {'first_name': self.first_name,
                'last_name': self.last_name,
                'email': self.email}

    @classmethod
    def create(cls, first_name, last_name, email, password):
        if not email or not first_name or not last_name or len(password) < 8:
            raise ValueError("User must have an email address")
        user = CustomUser(first_name=first_name, last_name=last_name, email=email, password=password)

        try:
            db.session.add(user)
            db.session.commit()
            return user
        except (ValueError, TypeError,IntegrityError):
            return None

    @classmethod
    def get_all(cls):
        users = cls.query.all()
        return users

    @classmethod
    def get_by_id(cls, pk):
        user = cls.query.get(pk)
        return user

    @classmethod
    def remove(cls, pk):
        try:
            user = cls.query.filter_by(id=pk)
            user.delete()
            db.session.commit()
        except db.error:
            return False
        return True

    def update(self, first_name=None, last_name=None, email=None):
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if email:
            self.email = email
        try:
            db.session.commit()
            return self
        except (ValueError, TypeError, IntegrityError):
            return None
