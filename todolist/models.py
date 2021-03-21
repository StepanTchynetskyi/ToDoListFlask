from sqlalchemy import MetaData
from app import db
from sqlalchemy.exc import IntegrityError
# metadata = MetaData()
# association_table = db.Table('association', metadata,
#                              db.Column('ToDoList_id', db.Integer, db.ForeignKey('ToDoList.id')),
#                              db.Column('CustomUser_id', db.Integer, db.ForeignKey('CustomUser.id'))
#                              )


class ToDoList(db.Model):
    __tablename__ = "ToDoList"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500))
    #members = db.relationship("CustomUser", secondary=association_table)
    members = db.Column(db.Integer)

    def __init__(self, name, description=None, members=None):
        self.name = name
        self.description = description
        self.members = members


    def __repr__(self):
        return f"<ToDoList_id {self.id}"

    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'description': self.description,
                }
                #'members': sorted([member.id for member in self.members.all()])

    @classmethod
    def create(cls, name, description='', members=None):
        try:
            todo_list = ToDoList(name=name, description=description)
            db.session.add(todo_list)
            db.session.commit()
            if members:
                todo_list.members.add(*members)
            return todo_list
        except (ValueError, TypeError,IntegrityError):
            # log error
            return None

    @classmethod
    def get_all(cls):
        todo_list = cls.query.all()
        return todo_list

    @classmethod
    def get_by_id(cls, pk):
        todo_list = cls.query.get(pk)
        return todo_list

    @classmethod
    def remove(cls, pk):
        try:
            todo_list = cls.query.filter_by(id=pk)
            todo_list.delete()
            db.session.commit()
        except db.error:
            return False
        return True

    def update1(self, name=None, description=None):
        try:
            if name:
                self.name = name
            if description:
                self.description = description
            db.session.commit()
            return self
        except (ValueError, TypeError,IntegrityError):
            return None

    def update_members(self, members_to_add=None, members_to_delete=None):
        try:
            if members_to_add:
                self.members.add(*members_to_add)
            if members_to_delete:
                self.members.remove(*members_to_delete)
            return self
        except (TypeError, ValueError,IntegrityError):
            return None


    def get_list_members(self):
        members = self.members.all()
        return members