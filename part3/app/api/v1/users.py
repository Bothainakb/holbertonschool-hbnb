from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='User password')
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user')
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
            created_user = facade.create_user(user_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return created_user.to_dict(), 201


@api.route('/<user_id>')
class UserResource(Resource):
    @api.doc('get_user')
    def get(self, user_id):
        """Fetch a single user by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @jwt_required()
    @api.expect(user_update_model)
    def put(self, user_id):
        """Modify user information (self only, excluding email/password)"""
        current_user = get_jwt_identity()

        # Check that the user_id in the URL matches the authenticated user
        if user_id != current_user:
            return {'error': 'Unauthorized action'}, 403

        user_data = api.payload

        # Prevent modifying email or password here
        if 'email' in user_data or 'password' in user_data:
            return {'error': 'You cannot modify email or password.'}, 400

        user = facade.update_user(user_id, user_data)
        if not user:
            return {'error': 'User not found'}, 404

        return user.to_dict(), 200
