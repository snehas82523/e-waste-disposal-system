# E-Waste disposal System

## Overview

This project is a web-based Information System designed to manage the lifecycle of electronic waste (E-Waste) recycling. It facilitates the process from a user submitting a pickup request, to an admin assigning it to an employee, and finally the employee collecting and processing the waste.

The system is built as a Single Page Application (SPA) using a Flask (Python) backend and a Vanilla JavaScript frontend, utilizing a RESTful API architecture.

## Live Demo
[View Live Site](https://sneha2025.pythonanywhere.com/)

## Features

* Public Portal: Users can submit pickup requests for their electronic waste.
* Admin Dashboard:

  * Secure Login/Logout.
  * Manage Employees: Create, List, Search, and Delete employees.
  * Manage Requests: View all requests and assign them to specific employees.
* Employee Portal: Employees can view their assigned tasks and update the status (Assigned -> Picked Up -> Recycled).
* Modern UI: Responsive design with a clean, eco-friendly aesthetic.

## Tech Stack

* Backend: Python, Flask, SQLAlchemy, SQLite.
* Frontend: HTML5, CSS3, JavaScript (Fetch API).
* Architecture: REST API.

---

## Requirements

### Functional Requirements

#### 1. Employee Management (CRUD)

* Create: Admin can add new employees with name, email, phone, role, and start date
* Read: Admin can view all employees and search by name
* Update: Employee status can be modified (Active/Inactive)
* Delete: Admin can remove employees from the system

#### 2. Pickup Request Management (CRUD)

* Create: Public users can submit pickup requests with item description and type
* Read: Admin and employees can view requests; users can track their requests
* Update: Admin can assign requests to employees; employees can update status
* Delete: Requests can be archived after completion

#### 3. User Management

* Create: System creates demo users for public submissions
* Read: Retrieve user information for request tracking
* Authentication: Admin login/logout functionality

#### 4. Request Assignment & Workflow

* Admin assigns pickup requests to specific employees
* Employees update request status through workflow stages:

  * Created -> Assigned -> Picked Up -> Delivered to Center -> Processed -> Closed

### Non-Functional Requirements

#### 1. Ease of Use

* Intuitive user interface with clear navigation
* Responsive design for desktop and mobile devices
* Real-time feedback for user actions
* Search and filter capabilities for data management

#### 2. Performance

* Fast page load times (< 2 seconds)
* Efficient database queries using SQLAlchemy ORM
* Asynchronous API calls for smooth user experience
* Minimal server response time for CRUD operations

#### 3. Data Integrity

* Foreign key constraints to maintain referential integrity
* Input validation on both frontend and backend
* Transaction rollback on errors
* Unique constraints on email fields
* Proper error handling and user feedback

#### 4. Security

* Session-based authentication for admin portal
* Password protection (demo uses plaintext; production should use hashing)
* SQL injection prevention through ORM
* CSRF protection via Flask sessions

---

## Data Model and ER Diagram

### Database Schema

#### User Table

| Field    | Type        | Constraints      | Description                      |
| -------- | ----------- | ---------------- | -------------------------------- |
| id       | Integer     | Primary Key      | Unique user identifier           |
| username | String(80)  | Not Null         | User's display name              |
| email    | String(120) | Unique, Not Null | User's email address             |
| password | String(120) | Not Null         | User password (should be hashed) |

#### Employee Table

| Field      | Type        | Constraints        | Description                |
| ---------- | ----------- | ------------------ | -------------------------- |
| id         | Integer     | Primary Key        | Unique employee identifier |
| name       | String(100) | Not Null           | Employee full name         |
| email      | String(120) | Unique, Not Null   | Employee email             |
| phone      | String(20)  | Optional           | Contact phone number       |
| role       | String(50)  | Default: Collector | Job role                   |
| status     | String(20)  | Default: Active    | Employment status          |
| start_date | String(20)  | Optional           | Employment start date      |

#### RecyclingCenter Table

| Field    | Type        | Constraints | Description              |
| -------- | ----------- | ----------- | ------------------------ |
| id       | Integer     | Primary Key | Unique center identifier |
| name     | String(100) | Not Null    | Center name              |
| location | String(200) | Optional    | Physical address         |

#### PickupRequest Table

| Field                | Type        | Constraints               | Description                 |
| -------------------- | ----------- | ------------------------- | --------------------------- |
| id                   | Integer     | Primary Key               | Unique request identifier   |
| user_id              | Integer     | Foreign Key (User.id)     | Requesting user             |
| item_description     | String(200) | Not Null                  | Description of e-waste item |
| item_type            | String(50)  | Default: Other            | Category of item            |
| status               | String(50)  | Default: Created          | Workflow status             |
| assigned_employee_id | Integer     | Foreign Key (Employee.id) | Assigned employee           |
| assigned_center_id   | Integer     | Foreign Key (Center.id)   | Assigned center             |
| created_at           | DateTime    | Auto-generated            | Request creation timestamp  |

### Entity Relationships

User (1) -> (M) PickupRequest
Employee (1) -> (M) PickupRequest
RecyclingCenter (1) -> (M) PickupRequest

---

## API Reference

### Employee Endpoints

#### GET /api/employees

Retrieve all employees.

#### POST /api/employees

Create a new employee.

#### DELETE /api/employees/{emp_id}

Delete an employee by ID.

### Pickup Request Endpoints

#### GET /api/requests

Retrieve all pickup requests.

#### POST /api/requests

Create a new pickup request.

#### PUT /api/requests/{req_id}/assign

Assign a request to an employee or recycling center.

#### PUT /api/requests/{req_id}/status

Update the status of a pickup request.

### User Endpoints

#### GET /api/users/{user_id}

Retrieve user information by ID.

---

## Installation and Setup

1. Ensure Python 3.7+ is installed.
2. Clone the repository and navigate to the project directory.
3. Install dependencies using requirements.txt.
4. Initialize the database.
5. Run the Flask application on [http://127.0.0.1:5001](http://127.0.0.1:5001).

---

## Usage Guide

### Public User

Submit pickup requests from the home page.

### Admin Portal

Login, manage employees, and assign pickup requests.

### Employee Portal

View assigned tasks and update request status.

---

## Testing

### Unit Tests

Covers Employee and Pickup Request CRUD operations, database integrity, and model serialization.

### Integration Test

Validates the complete workflow from request creation to closure.

---

## Project Structure

Describes the organization of backend, frontend, database, and testing files.

---

## Attribution

### Libraries and Frameworks

* **Flask** (v2.3.0+)

  * Web framework for Python
  * Used for: Routing, request handling, session management
  * License: BSD-3-Clause

* **Flask-SQLAlchemy** (v3.0.0+)

  * ORM extension for Flask
  * Used for: Database modeling, queries, and migrations
  * License: BSD-3-Clause

* **SQLite**

  * Embedded relational database
  * Used for: Data persistence and storage
  * License: Public Domain

---

### Frontend Resources

* **HTML5**

  * Markup structure

* **CSS3**

  * Styling and responsive design

* **Vanilla JavaScript**

  * Client-side interactivity and API calls

* **Fetch API**

  * Asynchronous HTTP requests

---

### Development Tools

* **Python** (v3.7+)

  * Programming language

* **Git**

  * Version control system

* **GitHub**

  * Repository hosting and collaboration

---

### Design Inspiration

* Modern eco-friendly color schemes
* Responsive card-based layouts
* Material Design principles for UI components

---

### Source Code

* **GitHub Repository**: [snehas82523/e-waste-disposal-system](https://github.com/snehas82523/e-waste-disposal-system.git)
