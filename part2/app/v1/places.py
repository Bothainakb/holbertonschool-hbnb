from flask import request
from flask_restx import Namespace, Resource

from app.services.facade import HBnBFacade
from app.models.place import Place

api = Namespace('places', description='Place operations')

facade = HBnBFacade()


@api.route('/')
class PlaceList(Resource):
    pass


@api.route('/<place_id>')
class PlaceResource(Resource):
    pass
