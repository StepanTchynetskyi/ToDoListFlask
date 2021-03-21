from datetime import date
from sqlalchemy.exc import IntegrityError
from app import db
from todolist.models import ToDoList


class Tasks(db.Model):
    __tablename__ = "Tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    is_completed = db.Column(db.Boolean(), default=False)
    deadline = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey("CustomUser.id"))
    list_id = db.Column(db.Integer, db.ForeignKey("ToDoList.id"))

    def __init__(self, title, description, is_completed=False, deadline=None, user=None, todolist=None):
        self.title = title
        self.description = description
        self.is_completed = is_completed
        self.deadline = deadline
        self.user = user
        self.todolist = todolist



    def __repr__(self):
        return f"<Tasks id {self.id}"

    def to_dict(self):
        return {'title': self.title,
                'description': self.description,
                'is_completed': self.is_completed,
                'deadline': self.deadline}

    @classmethod
    def get_all(cls):
        task = cls.query.all()
        return task

    @classmethod
    def get_by_id(cls, pk):
        task = cls.query.get(pk)
        return task

    @classmethod
    def remove(cls, pk):
        try:
            task = cls.query.filter_by(id=pk)
            task.delete()
            db.session.commit()
        except db.error:
            return False
        return True

    @classmethod
    def get_by_list_id(cls, list_id: int):
        tasks = Tasks.query.filter_by(list_id=list_id)
        return tasks

    @classmethod
    def create(cls,
               title: str,
               description: str,
               deadline: date,
               user_id:int,
               list_id: ToDoList):  # pylint disable=W0221
        task = Tasks(title=title, description=description, deadline=deadline)
        task.user = user_id
        task.todolist = list_id
        try:
            db.session.commit()
            return task
        except (ValueError, TypeError,IntegrityError):
            return None

    def update(self,
               title: str,
               description: str,
               is_completed: bool,
               deadline: date,
               user,
               todolist: ToDoList):  # pylint disable=W0221
        if title:
            self.title = title
        if description:
            self.description = description
        if deadline:
            self.deadline = deadline
        if is_completed:
            self.is_completed = is_completed
        if user:
            self.user = user
        if todolist:
            self.todolist = todolist
        try:
            db.session.commit()
            return True
        except (ValueError, IntegrityError):
            pass

