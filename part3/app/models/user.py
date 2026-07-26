import re
from flask_bcrypt import Bcrypt
from app.models.base import BaseModel

bcrypt = Bcrypt()


class User(BaseModel):
    # Class variable to store all users for uniqueness validation
    _all_users = []

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")
        self.is_admin = is_admin

        self.validate()
        User._all_users.append(self)

    def validate(self):
        """Validate user attributes according to requirements"""

        # Check first_name
        if not self.first_name or not self.first_name.strip():
            raise ValueError("First name cannot be empty")
        if len(self.first_name) > 50:
            raise ValueError("First name must not exceed 50 characters")

        # Check last_name
        if not self.last_name or not self.last_name.strip():
            raise ValueError("Last name cannot be empty")
        if len(self.last_name) > 50:
            raise ValueError("Last name must not exceed 50 characters")

        # Check email
        if not self.email or not self.email.strip():
            raise ValueError("Email cannot be empty")

        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, self.email):
            raise ValueError("Invalid email format")

        # Check email uniqueness
        for user in User._all_users:
            if user.email == self.email and user.id != self.id:
                raise ValueError(f"Email {self.email} is already in use")

    def to_dict(self):
        """Return a dictionary representation of the user"""
        data = super().to_dict()
        data.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        })
        return data

    def verify_password(self, password):
        """Verify a password against the stored hash"""
        return bcrypt.check_password_hash(self.password, password)
