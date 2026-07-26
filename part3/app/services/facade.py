from app.persistence.repository import InMemoryRepository
from app.models.user import User
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

    # ========== USER OPERATIONS ==========
    
    def create_user(self, user_data):
        """Create a new user"""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by ID"""
        return self.user_repo.get(user_id)

    def get_all_users(self):
        """Retrieve all users"""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update a user by ID"""
        user = self.user_repo.get(user_id)
        if user:
            user.update(user_data)
            return user
        return None

    def get_user_by_email(self, email):
        """Retrieve a user by email"""
        return self.user_repo.get_by_attribute('email', email)

    # ========== AMENITY OPERATIONS ==========
    
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
        """Update an amenity by ID"""
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            amenity.update(amenity_data)
            return amenity
        return None

    # ========== PLACE OPERATIONS ==========
    
    def create_place(self, place_data):
        """Create a new place"""
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieve a place by ID"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieve all places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place by ID"""
        place = self.place_repo.get(place_id)
        if place:
            place.update(place_data)
            return place
        return None

    # ========== REVIEW OPERATIONS ==========
    
    def create_review(self, review_data):
        """Create a new review"""
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Retrieve a review by ID"""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieve all reviews"""
        return self.review_repo.get_all()

    def update_review(self, review_id, review_data):
        """Update a review by ID"""
        review = self.review_repo.get(review_id)
        if review:
            review.update(review_data)
            return review
        return None

    def get_reviews_by_place(self, place_id):
        """Retrieve all reviews for a specific place"""
        place = self.place_repo.get(place_id)
        if place:
            return place.reviews
        return []
