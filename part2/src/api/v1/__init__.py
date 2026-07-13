from flask import Blueprint
from flask_restx import Api
from src.api.v1.users import api as users_ns
from src.api.v1.amenities import api as amenities_ns

v1_blueprint = Blueprint('api_v1', __name__, url_prefix='/api/v1')

api = Api(
    v1_blueprint,
    title='HBnB API',
    version='1.0',
    description='HBnB Application API',
    doc='/docs'
)

api.add_namespace(users_ns, path='/users')
api.add_namespace(amenities_ns, path='/amenities')
