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



if __name__ == '__main__':
    app.run()
