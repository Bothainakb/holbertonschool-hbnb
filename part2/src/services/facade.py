from src.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # === TASK 2: USER OPERATIONS ===
    def get_all_users(self):
        """Retrieve a list of all users from the repository"""
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        """Update user details in the repository and return the updated entity"""
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
        """Retrieve a user by their email address"""
        return self.user_repo.get_by_attribute('email', email)
        
    def get_user(self, user_id):
        """Retrieve a single user by their ID"""
        return self.user_repo.get(user_id)

    # === TASK 3: AMENITY OPERATIONS ===
    def create_amenity(self, amenity_data):
        """Create a new amenity and store it in the repository"""
        from src.models.amenity import Amenity
        
        new_amenity = Amenity(name=amenity_data['name'])
        self.amenity_repo.add(new_amenity)
        return new_amenity

    def get_amenity(self, amenity_id):
        """Retrieve a single amenity by its unique ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve a list of all amenities from the repository"""
        return self.amenity_repo.get_all()

    def get_amenity_by_name(self, name):
        """Retrieve an amenity by matching its name attribute"""
        return self.amenity_repo.get_by_attribute('name', name)

    def update_amenity(self, amenity_id, data):
        """Update an amenity's details and save changes to the repository"""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        
        if 'name' in data:
            amenity.name = data['name']
            
        self.amenity_repo.update(amenity_id, amenity)
        return amenity

facade = HBnBFacade()
