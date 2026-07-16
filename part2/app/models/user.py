import re
from app.models.base import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.validate()

    def validate(self):
        if not self.first_name or not self.first_name.strip():
            raise ValueError("First name cannot be empty")
        if not self.last_name or not self.last_name.strip():
            raise ValueError("Last name cannot be empty")
        if not self.email or not self.email.strip():
            raise ValueError("Email cannot be empty")
        
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, self.email):
            raise ValueError("Invalid email format")

    def to_dict(self):
        """Return a representation of User"""
        return{
                "id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email
                }
