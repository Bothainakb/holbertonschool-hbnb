# src/persistence/repository.py

class InMemoryRepository:
    def __init__(self):
        self._storage = {}

    def get_all(self):
        """Return all stored items as a list"""
        return list(self._storage.values())

    def get(self, obj_id):
        """Retrieve a single item by its ID"""
        return self._storage.get(obj_id)

    def update(self, obj_id, updated_obj):
        """Update an existing item in the storage"""
        if obj_id in self._storage:
            self._storage[obj_id] = updated_obj
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve an object by matching a specific attribute value (e.g., email)"""
        for obj in self._storage.values():
            # التأكد من أن الكائن يحتوي على الخاصية المطلوبة وتطابق القيمة
            if hasattr(obj, attr_name) and getattr(obj, attr_name) == attr_value:
                return obj
        return None
