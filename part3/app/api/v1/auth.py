from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import(
        create_access_token,
        get_jwt_identity,
        get_jwt
        )
from app.service import facade

 api = Namespace('auth',description='Authentication Operations')

 login_model = api.model('login',{
    'email':feilds.String(required=True,description='User email'),
    'password':feilds.String(required=True,description='User password')
    }) 

@api.route('/login')
  class Login(Resource):
 @api.expect(login_model)
    def post(self):
    """Authenticate user and return a JWT token"""
        credentials = api.payload

     #Retrieve the user based on the provided email
        user = facade.get_user_by_email(credentials['email'])

     #Check if user exists and the password is correct
        if not user or not user.vertify_password(credintials['password']):
            return {'error':'Invalid credintials'},401

     #create a JWT token with the user's id and is_admin flag
        access_token = create_access_token(
                identity=str(user.id),
                additional_claims={"is_admin":user.is_admin}
                )

    #return the JWT token to the client
        return {'access_token':access_token},200

@api.route('/protected')
    class ProtectedResource(Resource):
     @jwt_required()
        def get(self):
            """A protected endpoint that requires a valid JWT token"""
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            return {
                    'massage':f'Hello,user{current_user_id}',
                    'is_admin':claims.get('is_admin',False)},200
