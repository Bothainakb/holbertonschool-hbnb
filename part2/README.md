# HBnB Project - Part 2

## Overview
This project implements the three-layer architecture (Presentation, Business Logic, Persistence) for the HBnB application using a **Facade pattern** and an **In-Memory repository**. The Business Logic layer defines core entities and their relationships with comprehensive validation.

## Project Structure

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
```python
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
