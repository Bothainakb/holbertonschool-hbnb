import uuid
from datetime import datetime

from app import db


class BaseModel(db.Model):
    """Abstract base model for all SQLAlchemy models."""

    __abstract__ = True

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def save(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def update(self, data):
        """Update attributes from a dictionary."""
        for key, value in data.items():
            if (
                hasattr(self, key)
                and key not in ["id", "created_at", "updated_at"]
            ):
                setattr(self, key, value)

        self.save()

    def to_dict(self):
        """Return a dictionary representation of the model."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
