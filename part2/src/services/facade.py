# src/services/facade.py

class HBnBFacade:
    def __init__(self):
        # self.user_repo = UserRepository()  # تأكد من تفعيل السطر الخاص بمستودعك هنا
        pass

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

# السطر الأهم لربط الطبقات ببعضها بنجاح:
facade = HBnBFacade()
