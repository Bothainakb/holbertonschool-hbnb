import re
from flask_bcrypt import Bcrypt
from app import db
from app.models.base import BaseModel

bcrypt = Bcrypt()


class User(BaseModel):
    __tablename__ = "users"

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship(
        "Place",
        backref="owner",
        lazy=True,
        cascade="all, delete-orphan"
    )

    reviews = db.relationship(
        "Review",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")
        self.is_admin = is_admin

        self.validate()

    def validate(self):
        if not self.first_name or not self.first_name.strip():
            raise ValueError("First name cannot be empty")
        if len(self.first_name) > 50:
            raise ValueError("First name must not exceed 50 characters")
        if not self.last_name or not self.last_name.strip():
            raise ValueError("Last name cannot be empty")
        if len(self.last_name) > 50:
            raise ValueError("Last name must not exceed 50 characters")
        if not self.email or not self.email.strip():
            raise ValueError("Email cannot be empty")

        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, self.email):
            raise ValueError("Invalid email format")

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
