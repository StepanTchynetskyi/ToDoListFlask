from sqlalchemy import MetaData
from app import db

metadata = MetaData()
association_table = db.Table('association', metadata,
                             db.Column('ToDoList_id', db.Integer, db.ForeignKey('ToDoList.id')),
                             db.Column('CustomUser_id', db.Integer, db.ForeignKey('CustomUser.id'))
                             )


class ToDoList(db.Model):
    __tablename__ = "ToDoList"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500))
    members = db.relationship("CustomUser", secondary=association_table)

    def __init__(self, name, description=None, members=None):
        self.name = name
        self.description = description
        self.members = members
