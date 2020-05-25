# quartzapp.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quartzdatabase2.db'
app.secret_key = "flask rocks!"
bootstrap = Bootstrap(app)

db = SQLAlchemy(app)


if __name__ == '__main__':
     app.run
