# University Course Management System - FastAPI

This is a backend RESTful API built using **FastAPI** for managing a university system. It includes features to manage **students, courses, professors**, and **enrollments** using an in-memory dictionary as the database.

## Features

### Student Management

* Register, update, retrieve, and delete students
* View a student's enrolled courses
* GPA is automatically calculated when grades are updated

### Course Management

* Add, update, retrieve, and delete courses
* Assign professors to courses
* Enforce course capacity limits
* View students enrolled in a course (course roster)

### Professor Management

* Add, update, retrieve, and delete professors
* View courses assigned to a professor
* Cascading delete removes associated courses and enrollments if a professor is deleted

### Enrollment Management

* Enroll students in courses (with capacity check)
* Prevent duplicate enrollments
* Update grades
* Automatically update student GPA on grade update
* Drop courses

## Requirements

* Python 3.8+
* FastAPI
* Uvicorn
* Pydantic

Install dependencies:

```bash
pip install fastapi uvicorn
```

## Project Structure

```
project/
│
├── main.py           # FastAPI app with all routes
├── models.py         # Pydantic schemas for validation
├── database.py       # Dictionary-based in-memory storage
├── logic.py          # Business logic for GPA, capacity, validation
└── utils.py          # Optional helper functions
```

## How to Run

Start the development server:

```bash
uvicorn main:app --reload
```

Open your browser at:

```
http://127.0.0.1:8000/docs
```

Use the interactive Swagger UI to test all endpoints.

## Endpoints Summary

* `/students` — CRUD operations for students
* `/courses` — CRUD operations for courses
* `/professors` — CRUD operations for professors
* `/enrollments` — Manage course enrollments

## Notes

* The database is in-memory (non-persistent). Data will reset when the server restarts.
* Handles all core validation and business rules like GPA calculation and capacity enforcement.
