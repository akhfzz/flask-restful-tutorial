from flask_restful import Resource, reqparse, abort
from system import db
from models import Todo as MTodo
from system.auth import authenticate
from flask_jwt import jwt_required
from utils import abort_no_data, abort_no_arg

parser = reqparse.RequestParser()
parser.add_argument('task')

class Todo(Resource):
    method_decorators = [authenticate, jwt_required()]

    def __get(self, id):
        row = MTodo.query.filter_by(id=id).first()
        abort_no_data(id, row)
        return row

    def get(self, id):
        row = self.__get(id)
        return {
            'id': id,
            'task': row.task,
        }

    def delete(self, id):
        data = self.__get(id)
        db.session.delete(data)
        db.session.commit()
        return '', 204

    def put(self, id):
        data = self.__get(id)
        args = parser.parse_args()

        task = args['task'] if args['task'] else data.task

        data.task = task

        db.session.commit()

        return {
            'id': id,
            'task': task,
        }, 201

class TodoList(Resource):
    method_decorators = [authenticate, jwt_required()]

    def get(self):
        data = MTodo.query.all()
        data = [{
            'id': item.id,
            'task': item.task,
        } for item in data]
        return data

    def post(self):
        args = parser.parse_args()
        abort_no_arg('task', args)

        task = args['task']

        data = MTodo(task=task)
        db.session.add(data)
        db.session.commit()
        
        return {
            'id': data.id,
            'task': task,
        }, 201

config = {
    'name': 'Todo Entry-Point',
    'routes': {
        '': TodoList,
        '/<int:id>': Todo,
    },
}