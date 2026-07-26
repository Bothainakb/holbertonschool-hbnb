from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.models.user import User  

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    def get(self):
        """Fetch all users"""
        all_users = facade.get_all_users()
        return [user.to_dict() for user in all_users], 200

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or invalid data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Check for duplicate email using our facade
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            # 1. Instantiate the actual User model object
            new_user_obj = User(**user_data)
            # 2. Pass the created object to the facade
            created_user = facade.create_user(new_user_obj)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': created_user.id,
            'first_name': created_user.first_name,
            'last_name': created_user.last_name,
            'email': created_user.email
        }, 201
