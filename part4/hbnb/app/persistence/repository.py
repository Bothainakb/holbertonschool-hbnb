from abc import ABC, abstractmethod
from app import db


class Repository(ABC):
    """Abstract base class for data persistence repositories."""

    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class SQLAlchemyRepository(Repository):
    """Database repository implementing SQLAlchemy ORM operations."""

    def __init__(self, model):
        self.model = model

    def add(self, obj):
        """Add a new object to the database session and commit."""
        db.session.add(obj)
        db.session.commit()
        return obj

    def get(self, obj_id):
        """Fetch a single record by its Primary Key (UUID)."""
        return self.model.query.get(obj_id)

    def get_all(self):
        """Retrieve all records for this model."""
        return self.model.query.all()

    def update(self, obj_id, data):
        """Update object attributes and save to the database."""
        obj = self.get(obj_id)
        if obj:
            obj.update(data)
            db.session.commit()
        return obj

    def delete(self, obj_id):
        """Delete an object by ID from the database."""
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        """Filter records dynamically by attribute name and value."""
        return self.model.query.filter(
            getattr(self.model, attr_name) == attr_value
        ).first()


class InMemoryRepository(Repository):
    """In-memory repository for dictionary-based persistence."""

    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj
        return obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)
        return obj

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        return next(
            (
                obj for obj in self._storage.values()
                if getattr(obj, attr_name, None) == attr_value
            ),
            None
        )
