from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/to_do'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
CORS(app)

class To_do(db.Model):
   __tablename__ = "to_do"
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

todo1 = To_do(title="do work",description="time to study")
db.session.add(todo1)
db.session.commit()

# need to figure out a way to jsonify the things
@app.route('/')
def get_all():
   todo_list = [todo.json() for todo in To_do.query.all()]
   return jsonify(todo_list)
   

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
