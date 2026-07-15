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

        if float(data['price']) < 0:
            return {"error": "Price cannot be negative"}, 400

        if not (-90 <= float(data['latitude']) <= 90):
            return {"error": "Latitude must be between -90 and 90"}, 400

        if not (-180 <= float(data['longitude']) <= 180):
            return {"error": "Longitude must be between -180 and 180"}, 400

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
            "longitude": place.longitude,
            "owner": place.owner
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


@api.route('/<string:place_id>')
class PlaceResource(Resource):

    def get(self, place_id):
        place = facade.get_place(place_id)

        if place is None:
            return {"error": "Place not found"}, 404

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": place.owner
        }, 200

    def put(self, place_id):
        place = facade.get_place(place_id)

        if place is None:
            return {"error": "Place not found"}, 404

        data = request.get_json()

        if 'price' in data and float(data['price']) < 0:
            return {"error": "Price cannot be negative"}, 400

        if 'latitude' in data and not (-90 <= float(data['latitude']) <= 90):
            return {"error": "Latitude must be between -90 and 90"}, 400

        if 'longitude' in data and not (-180 <= float(data['longitude']) <= 180):
            return {"error": "Longitude must be between -180 and 180"}, 400

        facade.update_place(place_id, data)

        updated_place = facade.get_place(place_id)

        return {
            "id": updated_place.id,
            "title": updated_place.title,
            "description": updated_place.description,
            "price": updated_place.price,
            "latitude": updated_place.latitude,
            "longitude": updated_place.longitude,
            "owner": updated_place.owner
        }, 200
