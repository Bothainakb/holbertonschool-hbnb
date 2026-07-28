from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude')
})


@api.route('/')
class PlaceList(Resource):

    def get(self):
        """Retrieve a list of all places (public)"""
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200

    @jwt_required()
    @api.expect(place_model)
    def post(self):
        """Create a new place (authenticated users only)"""

        current_user = get_jwt_identity()
        data = api.payload

        if float(data['price']) < 0:
            return {"error": "Price cannot be negative"}, 400

        if not (-90 <= float(data['latitude']) <= 90):
            return {"error": "Latitude must be between -90 and 90"}, 400

        if not (-180 <= float(data['longitude']) <= 180):
            return {"error": "Longitude must be between -180 and 180"}, 400

        data['owner_id'] = current_user

        try:
            place = facade.create_place(data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return place.to_dict(), 201


@api.route('/<place_id>')
class PlaceResource(Resource):

    def get(self, place_id):
        """Retrieve detailed information about a specific place (public)"""

        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        return place.to_dict(), 200

    @jwt_required()
    @api.expect(place_model)
    def put(self, place_id):
        """
        Update a place.

        Owners can update their own places.
        Administrators can update any place.
        """

        current_user = get_jwt_identity()
        claims = get_jwt()

        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        if (
            not claims.get("is_admin")
            and place.owner.id != current_user
        ):
            return {"error": "Unauthorized action"}, 403

        data = api.payload

        if 'price' in data and float(data['price']) < 0:
            return {"error": "Price cannot be negative"}, 400

        if 'latitude' in data and not (-90 <= float(data['latitude']) <= 90):
            return {"error": "Latitude must be between -90 and 90"}, 400

        if 'longitude' in data and not (-180 <= float(data['longitude']) <= 180):
            return {"error": "Longitude must be between -180 and 180"}, 400

        updated_place = facade.update_place(place_id, data)

        if not updated_place:
            return {"error": "Place not found"}, 404

        return updated_place.to_dict(), 200
