from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80) unique=True, nullable=False)
    email = db.Column(db.String(80) unique=True, nullable=False)

    def __repr__(self):

@app.route('/')
def home():
    return '<h1>Hello, world!</h1>'

if __name__ == '__main__':
    app.run(port=8000, debug=True)