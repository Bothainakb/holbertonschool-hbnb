from app.models.base import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
        self.validate()

    def validate(self):
        """Validate review attributes according to requirements"""
        # Check text
        if not self.text or not self.text.strip():
            raise ValueError("Review text cannot be empty")
        
        # Check rating
        if self.rating is None:
            raise ValueError("Rating cannot be empty")
        try:
            rating_int = int(self.rating)
            if rating_int < 1 or rating_int > 5:
                raise ValueError("Rating must be between 1 and 5")
        except (TypeError, ValueError):
            raise ValueError("Rating must be an integer between 1 and 5")
        
        # Check place exists and is valid
        if self.place is None:
            raise ValueError("Place cannot be empty")
        from app.models.place import Place
        if not isinstance(self.place, Place):
            raise ValueError("Place must be a valid Place instance")
        
        # Check user exists and is valid
        if self.user is None:
            raise ValueError("User cannot be empty")
        from app.models.user import User
        if not isinstance(self.user, User):
            raise ValueError("User must be a valid User instance")

    def to_dict(self):
        """Return a dictionary representation of Review"""
        return {
            "id": self.id,
            "text": self.text,
            "rating": int(self.rating),
            "place_id": self.place.id,
            "user_id": self.user.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        } 
