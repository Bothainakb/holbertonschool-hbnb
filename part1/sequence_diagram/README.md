# Sequence Diagrams for HBnB API Calls

This directory contains the sequence diagrams representing the flow of interactions across the different layers of the HBnB application for four specific API calls.

## Architectural Layers Overview
* **Presentation Layer (API / Controller):** Receives the client request, validates auth tokens, and prepares the final HTTP response.
* **Business Logic Layer (Models / Services):** Processes business rules, validates incoming data models, and arranges actions.
* **Persistence Layer (Database):** Handles data storage, entity checks, and updates records in the database.

---

## 1. User Registration

### Purpose
Illustrates the workflow when a new user signs up for an account. It details how the system validates data, ensures the email is unique, hashes the password, and stores the user entity.

### Visual Diagram
```mermaid
sequenceDiagram
    autonumber
    actor User as User / Client
    participant Pres as Presentation Layer<br>(API / Controller)
    participant BL as Business Logic Layer<br>(UserModel / Service)
    participant DB as Persistence Layer<br>(Database)

    User->>Pres: POST /api/v1/users (Registration Data)
    activate Pres
    Pres->>BL: validate_user_data(data)
    activate BL
    BL->>DB: check_email_exists(email)
    activate DB
    DB-->>BL: Email is available
    deactivate DB
    
    BL->>BL: create_user_instance()
    BL->>BL: hash_password()
    
    BL->>DB: save_user(user_object)
    activate DB
    DB-->>BL: User saved successfully
    deactivate DB
    
    BL-->>Pres: UserCreated Object
    deactivate BL
    Pres-->>User: 201 Created (Success Message & User ID)
    deactivate Pres
```

---

## 2. Place Creation

### Purpose
Represents a host listing a new accommodation or place. It displays the authorization token check, owner validation, and saving the dynamic place object.

### Visual Diagram
```mermaid
sequenceDiagram
    autonumber
    actor User as Host / User
    participant Pres as Presentation Layer<br>(API / Controller)
    participant BL as Business Logic Layer<br>(PlaceModel / Service)
    participant DB as Persistence Layer<br>(Database)

    User->>Pres: POST /api/v1/places (Place Data + Auth Token)
    activate Pres
    Pres->>Pres: verify_token()
    Pres->>BL: validate_place_data(data)
    activate BL
    
    BL->>DB: verify_owner_exists(owner_id)
    activate DB
    DB-->>BL: Owner verified
    deactivate DB

    BL->>BL: create_place_instance()
    
    BL->>DB: save_place(place_object)
    activate DB
    DB-->>BL: Place saved successfully
    deactivate DB
    
    BL-->>Pres: Place Object
    deactivate BL
    Pres-->>User: 201 Created (Place Details)
    deactivate Pres
```

---

## 3. Review Submission

### Purpose
Captures how a guest evaluates and leaves a review for a specific place. It focuses on validating that both the target place and the voting user exist before linking the review.

### Visual Diagram
```mermaid
sequenceDiagram
    autonumber
    actor User as Guest / User
    participant Pres as Presentation Layer<br>(API / Controller)
    participant BL as Business Logic Layer<br>(ReviewModel / Service)
    participant DB as Persistence Layer<br>(Database)

    User->>Pres: POST /api/v1/places/{id}/reviews (Review Data)
    activate Pres
    Pres->>Pres: verify_token()
    Pres->>BL: validate_review_data(data)
    activate BL
    
    BL->>DB: verify_place_and_user(place_id, user_id)
    activate DB
    DB-->>BL: Verified (Place & User exist)
    deactivate DB

    BL->>BL: create_review_instance()
    
    BL->>DB: save_review(review_object)
    activate DB
    DB-->>BL: Review saved & linked to place
    deactivate DB
    
    BL-->>Pres: Review Object
    deactivate BL
    Pres-->>User: 201 Created (Review Confirmation)
    deactivate Pres
```

---

## 4. Fetching a List of Places

### Purpose
Details how users browse or search through available accommodations based on specific criteria filters, highlighting data formatting before returning the outcome.

### Visual Diagram
```mermaid
sequenceDiagram
    autonumber
    actor User as User / Client
    participant Pres as Presentation Layer<br>(API / Controller)
    participant BL as Business Logic Layer<br>(PlaceModel / Service)
    participant DB as Persistence Layer<br>(Database)

    User->>Pres: GET /api/v1/places?criteria=value
    activate Pres
    Pres->>BL: get_places(filters)
    activate BL
    
    BL->>DB: fetch_all_places(filters)
    activate DB
    DB-->>BL: List of Place Records
    deactivate DB
    
    BL->>BL: format_places_to_json()
    BL-->>Pres: Formatted Places List
    deactivate BL
    Pres-->>User: 200 OK (JSON array of places)
    deactivate Pres
```
