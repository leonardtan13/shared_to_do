from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/to_do'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
CORS(app)

class Todo(db.Model):
   __tablename__ = "todo"
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(256), nullable=False)
   description = db.Column(db.Text())
   done = db.Column(db.Boolean, default=False)

   def json(self):
       return {
           "id": self.id,
           "title": self.title,
           "description": self.description,
           "done" : self.done,
       }

db.drop_all()
db.create_all()

todo1 = Todo(title="do work",description="time to study")
db.session.add(todo1)
db.session.commit()


@app.route('/todo')
def get_all():
   todo_list = [todo.json() for todo in Todo.query.all()]
   return jsonify(todo_list)

@app.route('/todo', methods=["POST"])
def add_todo():
    data = request.get_json()
    newTodo = Todo(**data)
    try:
        db.session.add(newTodo)
        db.session.commit()
    except:
        return jsonify({
            "message": "error adding todo"
        }), 500
    return jsonify({
        "message" : "successfully added todo"
    }), 201

@app.route('/todo/<int:id>', methods=["DELETE"])
def delete_todo(id):
    todo = Todo.query.filter_by(id=id).first_or_404()
    try:
        db.session.delete(todo)
        db.session.commit
    except:
        return jsonify({
            "message": "error adding todo"
        }), 500
    return jsonify({
        "message" : "successfully deleted todo"
    }), 200

@app.route('/todo/<int:id>', methods = ['PUT'])
def update(id):
    data = request.get_json()
    todo = Todo.query.filter_by(id=id).first_or_404()
    if ("title" in data):
        todo.title = data["title"]
    if ("description" in data):
        todo.description = data["description"]
    if ("done" in data):
        todo.done = data["done"]
    try:
        db.session.commit()
    except:
        return jsonify({
            "message": "error updating todo"
        }), 500
    return jsonify({
        "message" : "successfully updated todo",
        "todo": todo.json()
    }), 200


    






   

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
