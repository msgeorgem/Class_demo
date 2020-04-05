import sys

from flask import Flask, render_template, request, jsonify, abort  # install with pip
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import expression

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://geo@localhost:5432/first_data_base'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)


## run flask db migrate in terminal after every change in ToDOo and then
## all changes re inmigrations/versions folder
## run flask db downgrade/upgrade

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    ##completed = db.Column(db.Boolean(), default=False, nullable=False)
    completed = db.Column(db.Boolean, server_default=expression.false(), nullable=False)  ## updated existing data


    # price = db.Column(db.Float, db.CheckConstraint('price>0'))
    # name = db.Column(db.String(), nullable=False, unique=True)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'


# db.create_all() ## wiil not be used if use migrations

@app.route('/todos/create', methods=['POST'])  # methods not method!!!
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)

@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())
