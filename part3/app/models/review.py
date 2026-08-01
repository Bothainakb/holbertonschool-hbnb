from app.models.base import BaseModel

class Review(BaseModel):
    __tablename = 'reviews'

    text = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), nullable=False)
    user_id = db.Column(db.String(36), nullable=False)

    def __init__(self, text, rating, place_id, user_id):
    
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id
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
        if not self.place_id:
            raise ValueError("Place cannot be empty")
        
        
        # Check user exists and is valid
        if not self.user_id:
            raise ValueError("User cannot be empty")
    

    def to_dict(self):
        """Return a dictionary representation of Review"""
        return {
            "id": self.id,
            "text": self.text,
            "rating": int(self.rating),
            "place_id": self.place_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        } 
