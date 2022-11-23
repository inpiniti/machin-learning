from flask import request
from flask_restx import Resource, Namespace

todos = {}
count = 1

Todo = Namespace('todo')

@Todo.route('/')
class TodoPost(Resource):
    def post(self):
        global count
        global todos

        idx = count
        count += 1
        todos[idx] = request.json.get('data')

        return {
            'todo_id': idx,
            'data': todos[idx]
        }

@Todo.route('/')
class TodoGet(Resource):
    def get(self):

        return todos

@Todo.route('/<int:todo_id>')
class TodoSimple(Resource):
    def get(self, todo_id):
        return {
            'todo_id': todo_id,
            'data': todos[todo_id]
        }

    def put(self, todo_id):
        todos[todo_id] = request.json.get('data')
        return {
            'todo_id': todo_id,
            'data': todos[todo_id]
        }

    def delete(self, todo_id):
        del todos[todo_id]
        return {
            "delete" : "success"
        }