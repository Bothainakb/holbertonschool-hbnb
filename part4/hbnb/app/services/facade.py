from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    """Service facade managing interaction between models and repositories."""

    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    # ==========================================
    # USER METHODS
    # ==========================================

    def create_user(self, user_data):
        """Create a new user instance and persist to DB."""
        user = User(**user_data)
        return self.user_repo.add(user)

    def get_user(self, user_id):
        """Retrieve user by ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Fetch user by unique email address."""
        return self.user_repo.get_by_attribute("email", email)

    def get_all_users(self):
        """Fetch all registered users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update existing user record."""
        return self.user_repo.update(user_id, user_data)

    def delete_user(self, user_id):
        """Delete user record."""
        return self.user_repo.delete(user_id)

    # ==========================================
    # PLACE METHODS
    # ==========================================

    def create_place(self, place_data):
        """Create and save a place instance."""
        place = Place(**place_data)
        return self.place_repo.add(place)

    def get_place(self, place_id):
        """Retrieve place by ID."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieve all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update place record."""
        return self.place_repo.update(place_id, place_data)

    def delete_place(self, place_id):
        """Delete place record."""
        return self.place_repo.delete(place_id)

    # ==========================================
    # AMENITY METHODS
    # ==========================================

    def create_amenity(self, amenity_data):
        """Create a new amenity record."""
        amenity = Amenity(**amenity_data)
        return self.amenity_repo.add(amenity)

    def get_amenity(self, amenity_id):
        """Retrieve amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update amenity record."""
        return self.amenity_repo.update(amenity_id, amenity_data)

    def delete_amenity(self, amenity_id):
        """Delete amenity record."""
        return self.amenity_repo.delete(amenity_id)

    def add_amenity_to_place(self, place_id, amenity_id):
        """Link an amenity to a place using many-to-many relationship."""
        place = self.get_place(place_id)
        amenity = self.get_amenity(amenity_id)

        if place and amenity:
            if amenity not in place.amenities:
                place.amenities.append(amenity)
                place.save()
            return True
        return False

    # ==========================================
    # REVIEW METHODS
    # ==========================================

    def create_review(self, review_data):
        """Create and save a review."""
        review = Review(**review_data)
        return self.review_repo.add(review)

    def get_review(self, review_id):
        """Retrieve review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieve all reviews."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Retrieve all reviews for a specific place."""
        place = self.get_place(place_id)
        return place.reviews if place else []

    def update_review(self, review_id, review_data):
        """Update review record."""
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        """Delete review record."""
        return self.review_repo.delete(review_id)

    facade = HBnBFacade()
