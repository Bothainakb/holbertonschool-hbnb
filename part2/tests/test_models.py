"""
Test suite for Business Logic Models

This module contains comprehensive tests for User, Place, Review, and Amenity classes
to validate that all attributes and relationships work correctly.
"""

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


# ============================================================================
# USER CLASS TESTS
# ============================================================================

def test_user_creation():
    """Test basic user creation"""
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False  # Default value
    assert user.id is not None
    assert user.created_at is not None
    assert user.updated_at is not None
    print("✓ User creation test passed!")


def test_user_first_name_max_length():
    """Test that first name cannot exceed 50 characters"""
    try:
        user = User(
            first_name="A" * 51,  # 51 characters
            last_name="Doe",
            email="john@example.com"
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "50 characters" in str(e)
        print("✓ First name max length validation passed!")


def test_user_last_name_max_length():
    """Test that last name cannot exceed 50 characters"""
    try:
        user = User(
            first_name="John",
            last_name="A" * 51,  # 51 characters
            email="john@example.com"
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "50 characters" in str(e)
        print("✓ Last name max length validation passed!")


def test_user_email_validation():
    """Test email format validation"""
    try:
        user = User(first_name="John", last_name="Doe", email="invalid-email")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Invalid email format" in str(e)
        print("✓ Email format validation passed!")


def test_user_email_uniqueness():
    """Test email uniqueness validation"""
    # Clear previous users for this test
    User._all_users.clear()
    
    user1 = User(first_name="John", last_name="Doe", email="john@example.com")
    try:
        user2 = User(first_name="Jane", last_name="Doe", email="john@example.com")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "already in use" in str(e)
        print("✓ Email uniqueness validation passed!")


def test_user_to_dict():
    """Test User to_dict method"""
    user = User(first_name="John", last_name="Doe", email="john@example.com", is_admin=True)
    user_dict = user.to_dict()
    assert user_dict["first_name"] == "John"
    assert user_dict["last_name"] == "Doe"
    assert user_dict["email"] == "john@example.com"
    assert user_dict["is_admin"] is True
    assert "id" in user_dict
    assert "created_at" in user_dict
    assert "updated_at" in user_dict
    print("✓ User to_dict test passed!")


# ============================================================================
# AMENITY CLASS TESTS
# ============================================================================

def test_amenity_creation():
    """Test basic amenity creation"""
    amenity = Amenity(name="Wi-Fi")
    assert amenity.name == "Wi-Fi"
    assert amenity.id is not None
    assert amenity.created_at is not None
    assert amenity.updated_at is not None
    print("✓ Amenity creation test passed!")


def test_amenity_name_max_length():
    """Test that amenity name cannot exceed 50 characters"""
    try:
        amenity = Amenity(name="A" * 51)  # 51 characters
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "50 characters" in str(e)
        print("✓ Amenity name max length validation passed!")


def test_amenity_empty_name():
    """Test that amenity name cannot be empty"""
    try:
        amenity = Amenity(name="")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "cannot be empty" in str(e)
        print("✓ Amenity empty name validation passed!")


def test_amenity_to_dict():
    """Test Amenity to_dict method"""
    amenity = Amenity(name="Parking")
    amenity_dict = amenity.to_dict()
    assert amenity_dict["name"] == "Parking"
    assert "id" in amenity_dict
    assert "created_at" in amenity_dict
    assert "updated_at" in amenity_dict
    print("✓ Amenity to_dict test passed!")


# ============================================================================
# PLACE CLASS TESTS
# ============================================================================

def test_place_creation():
    """Test basic place creation with valid data"""
    User._all_users.clear()
    owner = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    place = Place(
        title="Cozy Apartment",
        description="A nice place to stay",
        price=100.50,
        latitude=37.7749,
        longitude=-122.4194,
        owner=owner
    )
    assert place.title == "Cozy Apartment"
    assert place.price == 100.50
    assert place.latitude == 37.7749
    assert place.longitude == -122.4194
    assert place.owner == owner
    assert place.id is not None
    print("✓ Place creation test passed!")


def test_place_title_max_length():
    """Test that place title cannot exceed 100 characters"""
    User._all_users.clear()
    owner = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    try:
        place = Place(
            title="A" * 101,  # 101 characters
            description="Description",
            price=100,
            latitude=37.7749,
            longitude=-122.4194,
            owner=owner
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "100 characters" in str(e)
        print("✓ Place title max length validation passed!")


def test_place_price_positive():
    """Test that place price must be positive"""
    User._all_users.clear()
    owner = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    try:
        place = Place(
            title="Apartment",
            description="Description",
            price=-50,  # Negative price
            latitude=37.7749,
            longitude=-122.4194,
            owner=owner
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "positive" in str(e)
        print("✓ Place positive price validation passed!")


def test_place_latitude_range():
    """Test that place latitude must be between -90 and 90"""
    User._all_users.clear()
    owner = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    
    # Test too high
    try:
        place = Place(
            title="Apartment",
            description="Description",
            price=100,
            latitude=91,  # Out of range
            longitude=-122.4194,
            owner=owner
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Latitude" in str(e)
    
    # Test too low
    try:
        place = Place(
            title="Apartment",
            description="Description",
            price=100,
            latitude=-91,  # Out of range
            longitude=-122.4194,
            owner=owner
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Latitude" in str(e)
    
    print("✓ Place latitude range validation passed!")


def test_place_longitude_range():
    """Test that place longitude must be between -180 and 180"""
    User._all_users.clear()
    owner = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    
    # Test too high
    try:
        place = Place(
            title="Apartment",
            description="Description",
            price=100,
            latitude=37.7749,
            longitude=181  # Out of range
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Longitude" in str(e)
    
    print("✓ Place longitude range validation passed!")


def test_place_owner_validation():
    """Test that place owner must be a User instance"""
    try:
        place = Place(
            title="Apartment",
            description="Description",
            price=100,
            latitude=37.7749,
            longitude=-122.4194,
            owner="Not a User"  # Invalid owner
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "User instance" in str(e)
        print("✓ Place owner validation passed!")


def test_place_add_review():
    """Test adding reviews to a place"""
    User._all_users.clear()
    owner = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    place = Place(
        title="Cozy Apartment",
        description="A nice place to stay",
        price=100,
        latitude=37.7749,
        longitude=-122.4194,
        owner=owner
    )
    
    reviewer = User(first_name="Bob", last_name="Johnson", email="bob@example.com")
    review = Review(text="Great stay!", rating=5, place=place, user=reviewer)
    
    place.add_review(review)
    assert len(place.reviews) == 1
    assert place.reviews[0].text == "Great stay!"
    print("✓ Place add_review test passed!")


def test_place_add_amenity():
    """Test adding amenities to a place"""
    User._all_users.clear()
    owner = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    place = Place(
        title="Cozy Apartment",
        description="A nice place to stay",
        price=100,
        latitude=37.7749,
        longitude=-122.4194,
        owner=owner
    )
    
    amenity1 = Amenity(name="Wi-Fi")
    amenity2 = Amenity(name="Parking")
    
    place.add_amenity(amenity1)
    place.add_amenity(amenity2)
    
    assert len(place.amenities) == 2
    assert place.amenities[0].name == "Wi-Fi"
    assert place.amenities[1].name == "Parking"
    print("✓ Place add_amenity test passed!")


def test_place_to_dict():
    """Test Place to_dict method"""
    User._all_users.clear()
    owner = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    place = Place(
        title="Cozy Apartment",
        description="A nice place to stay",
        price=100.50,
        latitude=37.7749,
        longitude=-122.4194,
        owner=owner
    )
    
    amenity = Amenity(name="Wi-Fi")
    place.add_amenity(amenity)
    
    place_dict = place.to_dict()
    assert place_dict["title"] == "Cozy Apartment"
    assert place_dict["price"] == 100.50
    assert place_dict["latitude"] == 37.7749
    assert place_dict["longitude"] == -122.4194
    assert place_dict["owner_id"] == owner.id
    assert len(place_dict["amenity_ids"]) == 1
    assert "id" in place_dict
    print("✓ Place to_dict test passed!")


# ============================================================================
# REVIEW CLASS TESTS
# ============================================================================

def test_review_creation():
    """Test basic review creation"""
    User._all_users.clear()
    owner = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    place = Place(
        title="Cozy Apartment",
        description="A nice place",
        price=100,
        latitude=37.7749,
        longitude=-122.4194,
        owner=owner
    )
    
    reviewer = User(first_name="Bob", last_name="Johnson", email="bob@example.com")
    review = Review(text="Great stay!", rating=5, place=place, user=reviewer)
    
    assert review.text == "Great stay!"
    assert review.rating == 5
    assert review.place == place
    assert review.user == reviewer
    print("✓ Review creation test passed!")


def test_review_rating_range():
    """Test that review rating must be between 1 and 5"""
    User._all_users.clear()
    owner = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    place = Place(
        title="Cozy Apartment",
        description="A nice place",
        price=100,
        latitude=37.7749,
        longitude=-122.4194,
        owner=owner
    )
    reviewer = User(first_name="Bob", last_name="Johnson", email="bob@example.com")
    
    # Test too low
    try:
        review = Review(text="Bad stay", rating=0, place=place, user=reviewer)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "between 1 and 5" in str(e)
    
    # Test too high
    try:
        review = Review(text="Bad stay", rating=6, place=place, user=reviewer)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "between 1 and 5" in str(e)
    
    print("✓ Review rating range validation passed!")


def test_review_place_validation():
    """Test that review place must be a Place instance"""
    User._all_users.clear()
    user = User(first_name="Bob", last_name="Johnson", email="bob@example.com")
    
    try:
        review = Review(text="Great!", rating=5, place="Not a Place", user=user)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Place instance" in str(e)
        print("✓ Review place validation passed!")


def test_review_user_validation():
    """Test that review user must be a User instance"""
    User._all_users.clear()
    owner = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    place = Place(
        title="Cozy Apartment",
        description="A nice place",
        price=100,
        latitude=37.7749,
        longitude=-122.4194,
        owner=owner
    )
    
    try:
        review = Review(text="Great!", rating=5, place=place, user="Not a User")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "User instance" in str(e)
        print("✓ Review user validation passed!")


def test_review_to_dict():
    """Test Review to_dict method"""
    User._all_users.clear()
    owner = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    place = Place(
        title="Cozy Apartment",
        description="A nice place",
        price=100,
        latitude=37.7749,
        longitude=-122.4194,
        owner=owner
    )
    
    reviewer = User(first_name="Bob", last_name="Johnson", email="bob@example.com")
    review = Review(text="Great stay!", rating=5, place=place, user=reviewer)
    
    review_dict = review.to_dict()
    assert review_dict["text"] == "Great stay!"
    assert review_dict["rating"] == 5
    assert review_dict["place_id"] == place.id
    assert review_dict["user_id"] == reviewer.id
    assert "id" in review_dict
    print("✓ Review to_dict test passed!")


# ============================================================================
# RUN ALL TESTS
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("RUNNING COMPREHENSIVE MODEL TESTS")
    print("="*70 + "\n")
    
    print("USER TESTS:")
    print("-" * 70)
    test_user_creation()
    test_user_first_name_max_length()
    test_user_last_name_max_length()
    test_user_email_validation()
    test_user_email_uniqueness()
    test_user_to_dict()
    
    print("\nAMENITY TESTS:")
    print("-" * 70)
    test_amenity_creation()
    test_amenity_name_max_length()
    test_amenity_empty_name()
    test_amenity_to_dict()
    
    print("\nPLACE TESTS:")
    print("-" * 70)
    test_place_creation()
    test_place_title_max_length()
    test_place_price_positive()
    test_place_latitude_range()
    test_place_longitude_range()
    test_place_owner_validation()
    test_place_add_review()
    test_place_add_amenity()
    test_place_to_dict()
    
    print("\nREVIEW TESTS:")
    print("-" * 70)
    test_review_creation()
    test_review_rating_range()
    test_review_place_validation()
    test_review_user_validation()
    test_review_to_dict()
    
    print("\n" + "="*70)
    print("✓ ALL TESTS PASSED SUCCESSFULLY!")
    print("="*70 + "\n")
