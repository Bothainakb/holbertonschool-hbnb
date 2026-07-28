from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'place_id': fields.String(required=True, description='ID of the place being reviewed'),
    'text': fields.String(required=True, description='Content of the review'),
    'rating': fields.Integer(required=True, description='Rating from 1 to 5')
})


@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    def post(self):
        """Create a new review (authenticated users only)"""
        current_user = get_jwt_identity()
        review_data = api.payload

        place = facade.get_place(review_data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 404

        if place.owner.id == current_user:
            return {'error': 'You cannot review your own place.'}, 400

        for review in place.reviews:
            if review.user.id == current_user:
                return {'error': 'You have already reviewed this place.'}, 400

        review_data['user_id'] = current_user

        try:
            review = facade.create_review(review_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return review.to_dict(), 201


@api.route('/<review_id>')
class ReviewResource(Resource):
    @jwt_required()
    @api.expect(review_model)
    def put(self, review_id):
        """Update a review (only the review's author)"""
        current_user = get_jwt_identity()

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if review.user.id != current_user:
            return {'error': 'Unauthorized action'}, 403

        updated_review = facade.update_review(review_id, api.payload)
        return updated_review.to_dict(), 200

    @jwt_required()
    def delete(self, review_id):
        """Delete a review (only the review's author)"""
        current_user = get_jwt_identity()

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if review.user.id != current_user:
            return {'error': 'Unauthorized action'}, 403

        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200
