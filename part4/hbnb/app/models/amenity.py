from app import db
from app.models.base import BaseModel
from app.models.place import place_amenity


class Amenity(BaseModel):
    __tablename__ = "amenities"

    name = db.Column(db.String(50), nullable=False)

    places = db.relationship(
        "Place",
        secondary=place_amenity,
        lazy="subquery",
        backref=db.backref("amenities", lazy=True)
    )

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.validate()

    def validate(self):
        if not self.name or not self.name.strip():
            raise ValueError("Amenity name cannot be empty")
        if len(self.name) > 50:
            raise ValueError("Amenity name must not exceed 50 characters")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "place_ids": [place.id for place in self.places] if hasattr(self, 'places') else [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
