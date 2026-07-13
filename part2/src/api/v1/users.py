from flask import request
from flask_restx import Namespace, Resource, fields
from src.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'id': fields.String(description='The user unique identifier'),
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email address of the user')
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(required=False, description='Updated first name'),
    'last_name': fields.String(required=False, description='Updated last name'),
    'email': fields.String(required=False, description='Updated email address')
})


@api.route('/')
class UserList(Resource):
    
    @api.marshal_list_with(user_model)
    def get(self):
        users = facade.get_all_users()
        return users, 200


@api.route('/<string:user_id>')
@api.response(404, 'User not found')
class UserResource(Resource):

    @api.expect(user_update_model, validate=True)
    @api.marshal_with(user_model)
    def put(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, f"User with ID {user_id} not found")
        
        update_data = request.json
        
        if 'email' in update_data and update_data['email'] != user.email:
            existing_user = facade.get_user_by_email(update_data['email'])
            if existing_user:
                api.abort(400, "Email already in use")

        try:
            updated_user = facade.update_user(user_id, update_data)
            return updated_user, 200
        except ValueError as e:
            api.abort(400, str(e))
