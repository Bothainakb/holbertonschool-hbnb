from flask import request
from flask_restx import Namespace, Resource

from app.services.facade import HBnBFacade
from app.models.place import Place

api = Namespace('places', description='Place operations')

facade = HBnBFacade()


@api.route('/')
class PlaceList(Resource):

    def post(self):
        data = request.get_json()

        required_fields = [
            'title',
            'description',
            'price',
            'latitude',
            'longitude',
            'owner'
        ]

        for field in required_fields:
            if field not in data:
                return {"error": f"Missing {field}"}, 400

        place = Place(
            title=data['title'],
            description=data['description'],
            price=data['price'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            owner=data['owner']
        )

        facade.create_place(place)

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude
        }, 201
    
    def get(self):
    places = facade.get_all_places()

    return [
        {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": place.owner
        }
        for place in places
    ], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    pass
