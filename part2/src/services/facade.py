from src.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            user.email = data['email']
            
        self.user_repo.update(user_id, user)
        return user

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
        
    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def create_amenity(self, amenity_data):
        from src.models.amenity import Amenity
        
        new_amenity = Amenity(name=amenity_data['name'])
        self.amenity_repo.add(new_amenity)
        return new_amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def get_amenity_by_name(self, name):
        return self.amenity_repo.get_by_attribute('name', name)

    def update_amenity(self, amenity_id, data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        
        if 'name' in data:
            amenity.name = data['name']
            
        self.amenity_repo.update(amenity_id, amenity)
        return amenity

facade = HBnBFacade()
