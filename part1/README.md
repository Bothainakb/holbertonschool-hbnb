# HBnB Evolution - Part 1: UML Documentation

## Description

This project is the first phase of the HBnB Evolution application. The objective is to design the application's architecture and business logic using UML diagrams before implementation.

Project Overview:
 HBnB Evolution is a multi-tier accommodation marketplace application managing users, places, reviews, and amenities.

Purpose:
 This document establishes the architectural layout and object relationships prior to code implementation to ensure systemic consistency.

The documentation includes:

* High-Level Package Diagram
* Business Logic Class Diagram
* Sequence Diagrams for core API calls

The design follows a three-layer architecture:

* Presentation Layer
Manages public REST endpoints, parses user requests, and returns serialized HTTP status payloads.
* Business Logic Layer
Coordinates domain structures and runs state verification rules.
* Persistence Layer
Abstracts raw storage access using transactional databases.


The application models the following entities:

* User 
Tracks user credentials, email validation constraints, and host/guest authorization states.
* Place
Defines the accommodations listed by hosts; enforces positive coordinate and pricing boundaries.  
* Review
Handles textual and numeric feedback ratings submitted exclusively by verified past guests.
* Amenity
Standardizes globally shared property attributes.

### Design Choices and Rationale

 **The Facade Pattern Integration**
  The Presentation Layer interfaces exclusively with a unified Facade class sitting inside the Business Logic Layer. This decouples API routing handlers from internal subsystem changes, hides object instantiation complexities, and ensures core validation rules remain insulated.
  **Decoupled CRUD Operations**
  Communication between the Business Logic and Persistence Layers relies entirely on standardized CRUD repository abstractions. This isolates database storage routines, allowing back-end database changes to occur with zero modifications to the core business logic models.


## API Interaction Flow

### Runtime Layer Orchestration
To process API calls seamlessly without tight component coupling, requests traverse through clear system boundaries following this sequential lifecycle:

1. **Client** &rarr; Sends parameters to a public routing endpoint in the `PresentationLayer (API)`.
2. **API Controller** &rarr; Maps variables, sanitizes inputs, and calls the unified `Facade`.
3. **Facade Interface** &rarr; Forwards parameters to validate constraints inside the `BusinessLogicLayer`.
4. **Domain Entities** &rarr; Execute core business logic and delegate state mutations to the `PersistenceLayer`.
5. **Repository Engine** &rarr; Commits data changes safely to long-term storage (`Database`).

> **Diagram Reference:** The visual layouts detailing these precise method execution paths are located in `part1/sequence_diagrams/`.

## Team Members

* Albedah Bothaina
* Dana Alharbi
* Sarah Alburaidi

## Repository Structure

```text
part1/
├── package_diagram/
├── class_diagram/
├── sequence_diagrams/
└── README.md
```

## Objectives

* Design the system architecture using UML.
* Model the application's business entities and their relationships.
* Illustrate interactions between application layers.
* Provide documentation to guide future implementation.
