from app.persistence.repository import InMemoryRepository
from app.models.user import User, bcrypt
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    """
    Facade class that manages communication between the Presentation,
    Business Logic, and Persistence layers.
    """

    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ================= USER OPERATIONS =================

    def create_user(self, user_data):
        """Create a new user"""
        user = User(
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
            email=user_data.get("email"),
            password=user_data.get("password"),
            is_admin=user_data.get("is_admin", False)
        )

        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by ID"""
        return self.user_repo.get(user_id)

    def get_all_users(self):
        """Retrieve all users"""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update a user"""

        user = self.user_repo.get(user_id)

        if not user:
            return None

        # Hash a new password before storing it
        if "password" in user_data:
            user_data["password"] = bcrypt.generate_password_hash(
                user_data["password"]
            ).decode("utf-8")

        user.update(user_data)
        return user

    def get_user_by_email(self, email):
        """Retrieve a user by email"""
        return self.user_repo.get_by_attribute("email", email)

    # ================= AMENITY OPERATIONS =================

    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity"""

        amenity = self.amenity_repo.get(amenity_id)

        if not amenity:
            return None

        amenity.update(amenity_data)
        return amenity

    # ================= PLACE OPERATIONS =================

    def create_place(self, place_data):
        """Create a new place"""

        owner = self.get_user(place_data.get("owner_id"))

        if not owner:
            raise ValueError("Owner not found")

        place = Place(
            title=place_data.get("title"),
            description=place_data.get("description"),
            price=place_data.get("price"),
            latitude=place_data.get("latitude"),
            longitude=place_data.get("longitude"),
            owner=owner
        )

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieve a place by ID"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieve all places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place"""

        place = self.place_repo.get(place_id)

        if not place:
            return None

        place.update(place_data)
        return place

    # ================= REVIEW OPERATIONS =================

    def create_review(self, review_data):
        """Create a new review"""

        place = self.get_place(review_data.get("place_id"))
        user = self.get_user(review_data.get("user_id"))

        if not place or not user:
            raise ValueError("Invalid place or user")

        review = Review(
            text=review_data.get("text"),
            rating=review_data.get("rating"),
            place=place,
            user=user
        )

        self.review_repo.add(review)
        place.add_review(review)

        return review

    def get_review(self, review_id):
        """Retrieve a review by ID"""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieve all reviews"""
        return self.review_repo.get_all()

    def update_review(self, review_id, review_data):
        """Update a review"""

        review = self.review_repo.get(review_id)

        if not review:
            return None

        review.update(review_data)
        return review

    def delete_review(self, review_id):
        """Delete a review"""
        return self.review_repo.delete(review_id)

    def get_reviews_by_place(self, place_id):
        """Retrieve all reviews for a specific place"""

        place = self.place_repo.get(place_id)

        if not place:
            return []

        return place.reviews
