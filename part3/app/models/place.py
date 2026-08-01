from app.models.base import BaseModel
from app import db

class Place(BaseModel):
    __tablename__ = 'places'
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), nullable=False)

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
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
        if not self.owner_id:
            raise ValueError("Owner cannot be empty")

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
