from app import db


class Tasks(db.Model):
    __tablename__ = "Tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    is_completed = db.Column(db.Boolean(), default=False)
    deadline = db.Column(db.DateTime())
    user = db.relationship("CustomUser")
    todolist = db.relationship("ToDoList")


    def __init__(self, title, description, is_completed=False, deadline=None, user = None, todolist = None):
        self.title = title
        self.description = description
        self.is_completed = is_completed
        self.deadline = deadline
        self.user = user
        self.todolist = todolist

    def __repr__(self):
        return f"<Tasks id {self.id}"
