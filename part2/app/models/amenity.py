from app.models.base import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.validate()

    def validate(self):
    """Validate amenity attributes according to requirements"""
    if not self.name or not self.name.strip():
        raise ValueError("Amenity name cannot be empty")
    if len(self.name) > 50:
        raise ValueError("Amenity name must not exceed 50 characters")

    def to_dict(self):
    """Return a dictionary representation of Amenity"""
    return {
        "id": self.id,
        "name": self.name,
        "created_at": self.created_at.isoformat(),
        "updated_at": self.updated_at.isoformat()
    }
