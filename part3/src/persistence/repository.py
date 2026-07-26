class InMemoryRepository:
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        if hasattr(obj, 'id'):
            self._storage[obj.id] = obj
            return obj
        return None

    def get_all(self):
        return list(self._storage.values())

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def update(self, obj_id, updated_obj):
        if obj_id in self._storage:
            self._storage[obj_id] = updated_obj
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        for obj in self._storage.values():
            if hasattr(obj, attr_name) and getattr(obj, attr_name) == attr_value:
                return obj
        return None
