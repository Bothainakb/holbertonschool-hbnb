from app.models.base import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.validate()

    def validate(self):
        if not self.name or not self.name.strip():
            raise ValueError("Amenity name cannot be empty")
