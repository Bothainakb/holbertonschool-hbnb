# src/api/v1/amenities.py
from flask import request
from flask_restx import Namespace, Resource, fields
from src.services import facade

api = Namespace('amenities', description='Amenity operations')

# نموذج البيانات المرجعة والمدخلة للمرافق
amenity_model = api.model('Amenity', {
    'id': fields.String(description='The amenity unique identifier'),
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    
    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        """Create a new amenity"""
        amenity_data = request.json
        
        # التحقق من عدم تكرار اسم المرفق
        existing_amenity = facade.get_amenity_by_name(amenity_data['name'])
        if existing_amenity:
            api.abort(400, "Amenity name already exists")
            
        new_amenity = facade.create_amenity(amenity_data)
        return new_amenity, 201

    @api.marshal_list_with(amenity_model)
    def get(self):
        """Retrieve a list of all amenities"""
        return facade.get_all_amenities(), 200


@api.route('/<string:amenity_id>')
@api.response(404, 'Amenity not found')
class AmenityResource(Resource):

    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, f"Amenity with ID {amenity_id} not found")
        return amenity, 200

    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_model)
    def put(self, amenity_id):
        """Update an amenity's information by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, f"Amenity with ID {amenity_id} not found")
        
        update_data = request.json
        
        # التأكد من أن الاسم الجديد غير مستخدم في مرفق آخر
        if 'name' in update_data and update_data['name'] != amenity.name:
            existing_amenity = facade.get_amenity_by_name(update_data['name'])
            if existing_amenity:
                api.abort(400, "Amenity name already exists")

        updated_amenity = facade.update_amenity(amenity_id, update_data)
        return updated_amenity, 200
