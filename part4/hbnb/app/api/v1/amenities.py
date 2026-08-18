from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

amenity_update_model = api.model('AmenityUpdate', {
    'name': fields.String(required=True, description='New amenity name')
})


@api.route('/')
class AmenityList(Resource):

    def get(self):
        """Fetch all amenities"""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    def post(self):
        """Create a new amenity (Admin only)"""

        claims = get_jwt()

        if not claims.get("is_admin"):
            return {"error": "Administrator privileges required"}, 403

        amenity_data = api.payload

        try:
            amenity = facade.create_amenity(amenity_data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return amenity.to_dict(), 201


@api.route('/<amenity_id>')
class AmenityResource(Resource):

    def get(self, amenity_id):
        """Fetch an amenity by ID"""

        amenity = facade.get_amenity(amenity_id)

        if not amenity:
            return {"error": "Amenity not found"}, 404

        return amenity.to_dict(), 200

    @jwt_required()
    @api.expect(amenity_update_model, validate=True)
    def put(self, amenity_id):
        """Update an amenity (Admin only)"""

        claims = get_jwt()

        if not claims.get("is_admin"):
            return {"error": "Administrator privileges required"}, 403

        amenity = facade.update_amenity(
            amenity_id,
            api.payload
        )

        if not amenity:
            return {"error": "Amenity not found"}, 404

        return amenity.to_dict(), 200
