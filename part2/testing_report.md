# HBnB API - Testing Report

**Date:** July 16, 2026  
**Author:** dana
**Project Phase:** Part 2 (REST API Implementation)  

---

## 1. Executive Summary
This document provides a report of the test suite executed on the HBnB REST API. All endpoints (Users, Amenities, Places, and Reviews) have been covered. A total of **9 unit tests** were executed. 

*   **Total Tests Run:** 9
*   **Passed:** 9
*   **Failed:** 0
*   **Errors:** 0
*   **Status:** SUCCESS 

---

## 2. Test Suite Configuration & Run Command
The test suite utilizes Python's built-in `unittest` framework combined with Flask's test client to mock HTTP requests directly to the API application factory without spinning up a live server.

### Command to Execute Tests
```bash
python3 -m unittest discover -v -s tests
