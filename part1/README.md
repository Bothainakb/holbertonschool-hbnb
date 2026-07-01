# HBnB Evolution - Part 1: UML Documentation

## Description

This project is the first phase of the HBnB Evolution application. The objective is to design the application's architecture and business logic using UML diagrams before implementation.

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
racks user credentials, email validation constraints, and host/guest authorization states.
* Place
Defines the accommodations listed by hosts; enforces positive coordinate and pricing boundaries.
* Review
Handles textual and numeric feedback ratings submitted exclusively by verified past guests.
* Amenity
Standardizes globally shared property attributes (e.g., Wi-Fi, pool access).

## Team Members

* Albedah Bothaina
* Dana AlHarbi
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

