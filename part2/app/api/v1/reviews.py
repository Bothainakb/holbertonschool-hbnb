from flask import request
from flask_restx import Namespace, Resource

from app.services.facade import HBnBFacade
from app.models.review import Review

api = Namespace('reviews', description='Review operations')

facade = HBnBFacade()


@api.route('/')
class ReviewList(Resource):
    pass


@api.route('/<string:review_id>')
class ReviewResource(Resource):
    pass
