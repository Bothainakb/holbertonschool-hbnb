from flask import request
from flask_restx import Namespace, Resource

from app.services.facade import HBnBFacade
from app.models.review import Review

api = Namespace('reviews', description='Review operations')

facade = HBnBFacade()


@api.route('/')
class ReviewList(Resource):

    def post(self):
        data = request.get_json()

        required_fields = [
            'text',
            'rating',
            'place',
            'user'
        ]

        for field in required_fields:
            if field not in data:
                return {"error": f"Missing {field}"}, 400

        try:
            rating = int(data['rating'])
            if not (1 <= rating <= 5):
                return {"error": "Rating must be an integer between 1 and 5"}, 400
        except (ValueError, TypeError):
            return {"error": "Rating must be an integer between 1 and 5"}, 400

        review = Review(
            text=data['text'],
            rating=data['rating'],
            place=data['place'],
            user=data['user']
        )

        facade.create_review(review)

        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "place": review.place,
            "user": review.user
        }, 201

    def get(self):
        reviews = facade.get_all_reviews()

        return [
            {
                "id": review.id,
                "text": review.text,
                "rating": review.rating,
                "place": review.place,
                "user": review.user
            }
            for review in reviews
        ], 200


@api.route('/<string:review_id>')
class ReviewResource(Resource):

    def get(self, review_id):
        review = facade.get_review(review_id)

        if review is None:
            return {"error": "Review not found"}, 404

        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "place": review.place,
            "user": review.user
        }, 200

    def put(self, review_id):
        review = facade.get_review(review_id)

        if review is None:
            return {"error": "Review not found"}, 404

        data = request.get_json()

        if 'rating' in data:
            try:
                rating = int(data['rating'])
                if not (1 <= rating <= 5):
                    return {"error": "Rating must be an integer between 1 and 5"}, 400
            except (ValueError, TypeError):
                return {"error": "Rating must be an integer between 1 and 5"}, 400

        facade.update_review(review_id, data)

        updated_review = facade.get_review(review_id)

        return {
            "id": updated_review.id,
            "text": updated_review.text,
            "rating": updated_review.rating,
            "place": updated_review.place,
            "user": updated_review.user
        }, 200

    def delete(self, review_id):
        review = facade.get_review(review_id)

        if review is None:
            return {"error": "Review not found"}, 404

        facade.delete_review(review_id)

        return {"message": "Review deleted successfully"}, 200
