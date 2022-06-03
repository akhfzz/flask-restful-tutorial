from flask_restful import Resource
# from utils import response
from config import app

class Home(Resource):
    def get(self):
        return {
            'message': f'Selamat datang di {app.title}',
        }

config = {
    'name': 'Home',
    'routes': {
        '': Home,
    },
}