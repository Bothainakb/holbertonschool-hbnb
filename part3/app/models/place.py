from app.models.base import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities
        self.validate()

    def validate(self):
        """Validate place attributes according to requirements"""
        # Check title
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")
        if len(self.title) > 100:
            raise ValueError("Title must not exceed 100 characters")
        
        # Check price
        if self.price is None:
            raise ValueError("Price cannot be empty")
        try:
            price_float = float(self.price)
            if price_float <= 0:
                raise ValueError("Price must be a positive value")
        except (TypeError, ValueError):
            raise ValueError("Price must be a positive number")
        
        # Check latitude
        if self.latitude is None:
            raise ValueError("Latitude cannot be empty")
        try:
            lat_float = float(self.latitude)
            if lat_float < -90.0 or lat_float > 90.0:
                raise ValueError("Latitude must be between -90.0 and 90.0")
        except (TypeError, ValueError):
            raise ValueError("Latitude must be a valid number between -90.0 and 90.0")
        
        # Check longitude
        if self.longitude is None:
            raise ValueError("Longitude cannot be empty")
        try:
            lon_float = float(self.longitude)
            if lon_float < -180.0 or lon_float > 180.0:
                raise ValueError("Longitude must be between -180.0 and 180.0")
        except (TypeError, ValueError):
            raise ValueError("Longitude must be a valid number between -180.0 and 180.0")
        
        # Check owner exists
        if self.owner is None:
            raise ValueError("Owner cannot be empty")
        # Additional check: ensure owner is a User instance
        from app.models.user import User
        if not isinstance(self.owner, User):
            raise ValueError("Owner must be a valid User instance")

    def add_review(self, review):
        """Add a review to the place."""
        if review is None:
            raise ValueError("Review cannot be empty")
        # Optional: validate review is a Review instance
        from app.models.review import Review
        if not isinstance(review, Review):
            raise ValueError("Review must be a valid Review instance")
        if review not in self.reviews:
            self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        if amenity is None:
            raise ValueError("Amenity cannot be empty")
        # Optional: validate amenity is an Amenity instance
        from app.models.amenity import Amenity
        if not isinstance(amenity, Amenity):
            raise ValueError("Amenity must be a valid Amenity instance")
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def to_dict(self):
        """Return a dictionary representation of Place"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": float(self.price),
            "latitude": float(self.latitude),
            "longitude": float(self.longitude),
            "owner_id": self.owner.id,
            "amenity_ids": [amenity.id for amenity in self.amenities],
            "review_count": len(self.reviews),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
