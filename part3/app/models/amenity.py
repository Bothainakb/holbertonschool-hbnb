from app import db
from app.models.base import BaseModel
from app.models.place import place_amenity


class Amenity(BaseModel):
    __tablename__ = "amenities"

    name = db.Column(db.String(50), nullable=False)

    # Many-to-Many relationship with Place
    places = db.relationship(
        "Place",
        secondary=place_amenity,
        lazy="subquery",
        backref=db.backref("amenities", lazy=True)
    )

    def __init__(self, name):
        self.name = name
        self.validate()

    def validate(self):
        """Validate amenity attributes according to requirements."""

        if not self.name or not self.name.strip():
            raise ValueError("Amenity name cannot be empty")

        if len(self.name) > 50:
            raise ValueError("Amenity name must not exceed 50 characters")

    def to_dict(self):
        """Return a dictionary representation of Amenity."""

        return {
            "id": self.id,
            "name": self.name,
            "place_ids": [place.id for place in self.places],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
