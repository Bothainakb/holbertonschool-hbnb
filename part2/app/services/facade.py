from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User (Task 2)
    def create_user(self, user_data):
        pass

    # Place (Task 4)
    def create_place(self, place_data):
        pass

    def get_place(self, place_id):
        pass

    def get_all_places(self):
        pass

    def update_place(self, place_id, place_data):
        pass

    # Review (Task 5)
    def create_review(self, review_data):
        pass

    def get_review(self, review_id):
        pass

    def get_all_reviews(self):
        pass

    def update_review(self, review_id, review_data):
        pass

    def delete_review(self, review_id):
        pass

    def get_reviews_by_place(self, place_id):
        pass
