from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config
import os

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def hello():
    return "Hello World!"

from custom_users import user_view
from task import task_views
from todolist import list_views
app.register_blueprint(user_view.urlu)
app.register_blueprint(task_views.urlu)
app.register_blueprint(list_views.urlu)
if __name__ == '__main__':
    app.run()

