import unittest
import json
from app import create_app

class TestPlacesAndReviews(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.client.testing = True

        user_payload = {"first_name": "Sarah", "last_name": "Admin", "email": "sarah@example.com"}
        response = self.client.post('/api/v1/users/', json=user_payload)
        self.user_id = json.loads(response.data.decode()).get('id')

    def test_create_place_success(self):
        payload = {
            "title": "Luxury Apartment",
            "description": "A beautiful place to stay",
            "price": 150.0,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": self.user_id
        }
        response = self.client.post('/api/v1/places/', json=payload)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode())
        self.assertIn('id', data)

    def test_create_place_invalid_price(self):
        payload = {
            "title": "Cheap Room",
            "price": -10.0,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": self.user_id
        }
        response = self.client.post('/api/v1/places/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_get_place_not_found(self):
        response = self.client.get('/api/v1/places/invalid-id-123')
        self.assertEqual(response.status_code, 404)

    def test_create_review_success(self):
        place_payload = {
            "title": "Cozy Cabin",
            "price": 99.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": self.user_id
        }
        place_resp = self.client.post('/api/v1/places/', json=place_payload)
        place_id = json.loads(place_resp.data.decode()).get('id')

        review_payload = {
            "text": "Amazing experience, highly recommended!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": place_id
        }
        response = self.client.post('/api/v1/reviews/', json=review_payload)
        self.assertEqual(response.status_code, 201)

    def test_create_review_invalid_rating(self):
        review_payload = {
            "text": "Terrible",
            "rating": 6,
            "user_id": self.user_id,
            "place_id": "some-place-id"
        }
        response = self.client.post('/api/v1/reviews/', json=review_payload)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
