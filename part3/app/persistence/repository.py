from abc import ABC, abstractmethod


class Repository(ABC):
    """Abstract base class for repository pattern"""
    
    @abstractmethod
    def add(self, obj):
        """Add an object to the repository"""
        pass

    @abstractmethod
    def get(self, obj_id):
        """Retrieve an object by ID"""
        pass

    @abstractmethod
    def get_all(self):
        """Retrieve all objects"""
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """Update an object by ID"""
        pass

    @abstractmethod
    def delete(self, obj_id):
        """Delete an object by ID"""
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve an object by attribute value"""
        pass


class InMemoryRepository(Repository):
    """In-memory repository implementation for storing objects"""
    
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        """Add an object to the repository"""
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """Retrieve an object by ID"""
        return self._storage.get(obj_id)

    def get_all(self):
        """Retrieve all objects"""
        return list(self._storage.values())

    def update(self, obj_id, data):
        """Update an object by ID"""
        obj = self.get(obj_id)
        if obj:
            obj.update(data)
            return obj
        return None

    def delete(self, obj_id):
        """Delete an object by ID"""
        if obj_id in self._storage:
            del self._storage[obj_id]
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve the first object with a specific attribute value"""
        return next((obj for obj in self._storage.values() 
                    if getattr(obj, attr_name, None) == attr_value), None)
