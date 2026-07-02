# HBnB Evolution - Part 1: UML Documentation

## Description

This project is the first phase of the HBnB Evolution application. The objective is to design the application's architecture and business logic using UML diagrams before implementatation.

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
* Place
* Review
* Amenity


### Design Choices and Rationale

 **The Facade Pattern Integration**
  The Presentation Layer interfaces exclusively with a unified Facade class sitting inside the Business Logic Layer. This decouples API routing handlers from internal subsystem changes, hides object instantiation complexities, and ensures core validation rules remain insulated.
  **Decoupled CRUD Operations**
  Communication between the Business Logic and Persistence Layers relies entirely on standardized CRUD repository abstractions. This isolates database storage routines, allowing back-end database changes to occur with zero modifications to the core business logic models.


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
