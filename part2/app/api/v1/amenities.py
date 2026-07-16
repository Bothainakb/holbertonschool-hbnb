from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.models.amenity import Amenity  

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid data')
    def post(self):
        """Create a new amenity"""
        amenity_data = api.payload

        try:
            # 1. Instantiate the actual Amenity model object
            new_amenity_obj = Amenity(**amenity_data)
            # 2. Pass the created object to the facade
            created_amenity = facade.create_amenity(new_amenity_obj)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': created_amenity.id,
            'name': created_amenity.name
        }, 201
