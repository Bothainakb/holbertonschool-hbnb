from app import db
from app.models.base import BaseModel

place_amenity = db.Table(
    "place_amenity",
    db.Column("place_id", db.String(36), db.ForeignKey("places.id"), primary_key=True),
    db.Column("amenity_id", db.String(36), db.ForeignKey("amenities.id"), primary_key=True)
)


class Place(BaseModel):
    __tablename__ = "places"

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    owner_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=False
    )

    reviews = db.relationship(
        "Review",
        backref="place",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id

        self.validate()

    def validate(self):
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")
        if len(self.title) > 100:
            raise ValueError("Title must not exceed 100 characters")

        if self.price is None:
            raise ValueError("Price cannot be empty")
        try:
            if float(self.price) <= 0:
                raise ValueError("Price must be positive")
        except (TypeError, ValueError):
            raise ValueError("Price must be a positive number")

        if self.latitude is None:
            raise ValueError("Latitude cannot be empty")
        try:
            lat = float(self.latitude)
            if lat < -90 or lat > 90:
                raise ValueError("Latitude must be between -90 and 90")
        except (TypeError, ValueError):
            raise ValueError("Latitude must be a valid number")

        if self.longitude is None:
            raise ValueError("Longitude cannot be empty")
        try:
            lon = float(self.longitude)
            if lon < -180 or lon > 180:
                raise ValueError("Longitude must be between -180 and 180")
        except (TypeError, ValueError):
            raise ValueError("Longitude must be a valid number")

        if not self.owner_id:
            raise ValueError("Owner cannot be empty")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "amenity_ids": [amenity.id for amenity in self.amenities] if hasattr(self, 'amenities') else [],
            "review_count": len(self.reviews) if hasattr(self, 'reviews') else 0,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
