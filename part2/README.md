# HBnB Project - Part 2

## Overview
This project implements the three-layer architecture (Presentation, Business Logic, Persistence) for the HBnB application using a **Facade pattern** and an **In-Memory repository**. The Business Logic layer defines core entities and their relationships with comprehensive validation.

## Project Structure
part2/ ├── app/ │ ├── init.py # Flask app initialization │ ├── models/ │ │ ├── init.py │ │ ├── base.py # BaseModel class (UUID, timestamps) │ │ ├── user.py # User entity │ │ ├── place.py # Place entity │ │ ├── review.py # Review entity │ │ └── amenity.py # Amenity entity │ ├── persistence/ │ │ ├── init.py │ │ └── repository.py # In-memory repository pattern │ ├── services/ │ │ ├── init.py │ │ └── facade.py # Facade pattern (Business Logic interface) │ └── api/ │ └── v1/ # API endpoints ├── tests/ │ └── test_models.py # Comprehensive test suite (24 tests) ├── config.py # Configuration settings ├── requirements.txt # Project dependencies ├── run.py # Application entry point └── 
R
## Business Logic Layer

The Business Logic layer manages core entities and their relationships. Each entity inherits from `BaseModel` which provides:
- **UUID-based identification** (globally unique)
- **Timestamps** (created_at, updated_at)
- **Save and update methods**

### Entities

#### **User**
Represents a user in the system.

**Attributes:**
- `id` (String): Unique identifier
- `first_name` (String): Max 50 characters, required
- `last_name` (String): Max 50 characters, required
- `email` (String): Unique, required, must be valid email format
- `is_admin` (Boolean): Admin privileges flag (default: False)
- `created_at` (DateTime): Timestamp of creation
- `updated_at` (DateTime): Timestamp of last update

**Validations:**
- Email format validation (regex pattern)
- Email uniqueness across all users
- Character length constraints (50 max for names)

**Methods:**
- `validate()`: Validates all user attributes
- `to_dict()`: Returns dictionary representation

**Example Usage:**
from app.models.user import User

# Create a new user
user = User(
    first_name="John",
    last_name="Doe",
    email="john.doe@example.com",
    is_admin=False
)

# Access attributes
print(user.first_name)  # "John"
print(user.email)       # "john.doe@example.com"

# Convert to dictionary
user_dict = user.to_dict()
Place
Represents a place/property that can be rented.

Attributes:

id (String): Unique identifier
title (String): Max 100 characters, required
description (String): Optional detailed description
price (Float): Nightly price, must be positive
latitude (Float): Location latitude (-90.0 to 90.0)
longitude (Float): Location longitude (-180.0 to 180.0)
owner (User): User instance who owns the place
reviews (List): Related Review objects
amenities (List): Related Amenity objects
created_at (DateTime): Timestamp of creation
updated_at (DateTime): Timestamp of last update
Validations:

Title length (max 100 characters)
Price must be positive
Latitude in valid range (-90 to 90)
Longitude in valid range (-180 to 180)
Owner must be a User instance
Methods:

validate(): Validates all place attributes
add_review(review): Adds a review to the place
add_amenity(amenity): Adds an amenity to the place
to_dict(): Returns dictionary representation
Example Usage:


from app.models.place import Place
from app.models.user import User
from app.models.amenity import Amenity

# Create a place
owner = User(first_name="Alice", last_name="Smith", email="alice@example.com")
place = Place(
    title="Cozy Apartment",
    description="A beautiful place in the city",
    price=150.00,
    latitude=37.7749,
    longitude=-122.4194,
    owner=owner
)

# Add amenities
wifi = Amenity(name="Wi-Fi")
parking = Amenity(name="Parking")
place.add_amenity(wifi)
place.add_amenity(parking)
Review
Represents a review/rating for a place.

Attributes:

id (String): Unique identifier
text (String): Review content, required
rating (Integer): Rating (1-5), required
place (Place): Place being reviewed
user (User): User who wrote the review
created_at (DateTime): Timestamp of creation
updated_at (DateTime): Timestamp of last update
Validations:

Rating must be between 1 and 5
Place must be a Place instance
User must be a User instance
Text must not be empty
Methods:

validate(): Validates all review attributes
to_dict(): Returns dictionary representation
Example Usage:


from app.models.review import Review

# Create a review
reviewer = User(first_name="Bob", last_name="Johnson", email="bob@example.com")
review = Review(
    text="Amazing place! Very comfortable and clean.",
    rating=5,
    place=place,
    user=reviewer
)

# Add review to place
place.add_review(review)
Amenity
Represents an amenity (feature) available at a place.

Attributes:

id (String): Unique identifier
name (String): Amenity name (e.g., "Wi-Fi", "Pool"), max 50 characters
created_at (DateTime): Timestamp of creation
updated_at (DateTime): Timestamp of last update
Validations:

Name length (max 50 characters)
Name cannot be empty
Methods:

validate(): Validates all amenity attributes
to_dict(): Returns dictionary representation
Example Usage:


from app.models.amenity import Amenity

# Create amenities
wifi = Amenity(name="Wi-Fi")
pool = Amenity(name="Pool")
parking = Amenity(name="Parking")

# Convert to dictionary
amenity_dict = wifi.to_dict()
Relationships
The Business Logic layer implements the following relationships:


User ──── (owns) ──→ Place
                      ↓
                    Review ←──── (writes) ──── User

Place ─── (has many) ──→ Amenity (many-to-many via list)
User → Place (one-to-many): A user can own multiple places
Place → Review (one-to-many): A place can have multiple reviews
Place → Amenity (many-to-many): A place can have multiple amenities
Review → User (many-to-one): A review is written by one user
Review → Place (many-to-one): A review is for one place
Facade Pattern
The HBnBFacade class provides a unified interface to the Business Logic layer:

User Operations:

create_user(user_data): Create a new user
get_user(user_id): Retrieve user by ID
get_all_users(): Retrieve all users
update_user(user_id, user_data): Update user
get_user_by_email(email): Retrieve user by email
Amenity Operations:

create_amenity(amenity_data): Create a new amenity
get_amenity(amenity_id): Retrieve amenity by ID
get_all_amenities(): Retrieve all amenities
update_amenity(amenity_id, amenity_data): Update amenity
Place Operations:

create_place(place_data): Create a new place
get_place(place_id): Retrieve place by ID
get_all_places(): Retrieve all places
update_place(place_id, place_data): Update place
Review Operations:

create_review(review_data): Create a new review
get_review(review_id): Retrieve review by ID
get_all_reviews(): Retrieve all reviews
update_review(review_id, review_data): Update review
get_reviews_by_place(place_id): Get all reviews for a place
Persistence Layer
The persistence layer uses an In-Memory Repository pattern:

Repository: Abstract base class defining CRUD operations
InMemoryRepository: Concrete implementation storing objects in a dictionary
No database required for basic functionality
Easy to extend with database support later
Testing
The project includes a comprehensive test suite with 24 tests covering:

Entity creation and attribute assignment
All validation rules and edge cases
Relationship management
Serialization (to_dict methods)
Character length boundaries
Range validations for coordinates
Email format and uniqueness
Run tests:

bash
python part2/tests/test_models.py
Expected output:


======================================================================
RUNNING COMPREHENSIVE MODEL TESTS
======================================================================

USER TESTS:
----------------------------------------------------------------------
✓ User creation test passed!
✓ First name max length validation passed!
✓ Last name max length validation passed!
✓ Email format validation passed!
✓ Email uniqueness validation passed!
✓ User to_dict test passed!

AMENITY TESTS:
----------------------------------------------------------------------
✓ Amenity creation test passed!
✓ Amenity name max length validation passed!
✓ Amenity empty name validation passed!
✓ Amenity to_dict test passed!

PLACE TESTS:
----------------------------------------------------------------------
✓ Place creation test passed!
✓ Place title max length validation passed!
✓ Place positive price validation passed!
✓ Place latitude range validation passed!
✓ Place longitude range validation passed!
✓ Place owner validation passed!
✓ Place add_review test passed!
✓ Place add_amenity test passed!
✓ Place to_dict test passed!

REVIEW TESTS:
----------------------------------------------------------------------
✓ Review creation test passed!
✓ Review rating range validation passed!
✓ Review place validation passed!
✓ Review user validation passed!
✓ Review to_dict test passed!

======================================================================
✓ ALL TESTS PASSED SUCCESSFULLY!
======================================================================
Installation
Install dependencies:


pip install -r requirements.txt
Run the application:

python run.py
Architecture Layers
1. Business Logic Layer ✅
Defines entities (User, Place, Review, Amenity)
Implements validation rules
Manages relationships
Current status: Fully implemented
2. Persistence Layer ✅
In-memory repository pattern
CRUD operations
Current status: Fully implemented
3. Service Layer ✅
Facade pattern for unified interface
Current status: Fully implemented
4. Presentation Layer (API)
Flask-RESTx endpoints
Status: To be implemented in future tasks
Key Features
✅ UUID-based identification - Globally unique IDs for all entities ✅ Timestamp tracking - created_at and updated_at for all entities ✅ Comprehensive validation - All entity attributes are validated ✅ Relationship management - One-to-many and many-to-many relationships ✅ Facade pattern - Clean interface to business logic ✅ In-memory persistence - No database overhead for prototyping ✅ Extensive testing - 24 comprehensive tests with 100% coverage

Next Steps
Implement API endpoints (Presentation layer)
Add database support (replace in-memory repository)
Implement authentication and authorization
Add advanced search and filtering features
Implement user authentication with JWT token 

Authors
Sarah, Bothina and Dana
