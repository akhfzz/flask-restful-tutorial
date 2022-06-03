from flask_restful import Resource, reqparse, abort
# from utils import response
from system import db
from models import Product as MProduct
from system.auth import authenticate
from flask_jwt import jwt_required, current_identity
from utils import abort_no_data, abort_no_arg

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('desc')
parser.add_argument('price', type=float)
parser.add_argument('stock', type=int)

class Product(Resource):
    method_decorators = [authenticate, jwt_required()]

    def __get(self, id):
        row = MProduct.query.filter_by(id=id).first()
        abort_no_data(id, row)
        return row

    def get(self, id):
        row = self.__get(id)
        return {
            'id': id,
            'name': row.name,
            'desc': row.desc,
            'price': float(row.price),
            'stock': int(row.stock),
        }

    def delete(self, id):
        if current_identity.username == 'test':
            abort(403)
        data = self.__get(id)
        db.session.delete(data)
        db.session.commit()
        return '', 204

    def put(self, id):
        data = self.__get(id)
        args = parser.parse_args()

        name = args['name'] if args['name'] else data.name
        desc = args['desc'] if args['desc'] else data.desc
        price = float(args['price'] if args['price'] else data.price)
        stock = int(args['stock'] if args['stock'] else data.stock)

        data.name = name
        data.desc = desc
        data.price = price
        data.stock = stock

        db.session.commit()

        return {
            'id': id,
            'name': name,
            'desc': desc,
            'price': price,
            'stock': stock,
        }, 201

class ProductList(Resource):
    method_decorators = [authenticate, jwt_required()]

    def get(self):
        data = MProduct.query.all()
        data = [{
            'id': item.id,
            'name': item.name,
            'desc': item.desc,
            'price': float(item.price),
            'stock': item.stock,
        } for item in data]
        return data

    def post(self):
        args = parser.parse_args()
        abort_no_arg('name', args)
        abort_no_arg('price', args)

        name = args['name']
        desc = args['desc'] if args['desc'] else None
        price = float(args['price'])
        stock = int(args['stock']) if args['stock'] else 0

        data = MProduct(name=name, desc=desc, price=price, stock=stock)
        db.session.add(data)
        db.session.commit()
        
        return {
            'id': data.id,
            'name': name,
            'desc': desc,
            'price': price,
            'stock': stock,
        }, 201

config = {
    'name': 'Product Entry-Point',
    'routes': {
        '': ProductList,
        '/<int:id>': Product,
    },
}