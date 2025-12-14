# E-Waste disposal and reward System

## Overview

This project is a web-based Information System designed to manage the lifecycle of electronic waste (E-Waste) recycling. It facilitates the process from a user submitting a pickup request, to an admin assigning it to an employee, and finally the employee collecting and processing the waste.

The system is built as a Single Page Application (SPA) using a Flask (Python) backend and a Vanilla JavaScript frontend, utilizing a RESTful API architecture.

## Live Demo
[View Live Site](https://sneha2025.pythonanywhere.com/)

## Features

* **Public Portal & User Dashboard**:
  * **Landing Page**: Clean, modern interface prompting users to recycle.
  * **User Registration & Login**: Secure account creation.
  * **Dedicated Dashboard**: Users have a personal dashboard to submit pickup requests and track them in real-time.
  * **Request Tracking**: detailed status updates (Created -> Assigned -> Picked Up -> Recycled).
* **Admin Dashboard**:
  * Secure Login/Logout.
  * **Manage Employees**: Create, List, Search, and Delete employees.
  * **Manage Requests**: View all requests and assign them to specific employees.
* **Employee Portal**: Employees can view their assigned tasks and update the status (Assigned -> Picked Up -> Recycled).
* **Modern UI**: Responsive design with a clean, eco-friendly aesthetic.

## Tech Stack

* **Backend**: Python, Flask, SQLAlchemy, SQLite.
* **Frontend**: HTML5, CSS3, JavaScript (Fetch API).
* **Architecture**: REST API.

---

## Requirements

### Functional Requirements

#### 1. Employee Management (CRUD)
* Create: Admin can add new employees with name, email, phone, role, and start date
* Read: Admin can view all employees and search by name
* Update: Employee status can be modified (Active/Inactive)
* Delete: Admin can remove employees from the system

#### 2. Pickup Request Management (CRUD)
* Create: Public users can submit pickup requests via their dashboard
* Read: Admin and employees can view requests; users can track their specific requests
* Update: Admin can assign requests to employees; employees can update status
* Delete: Requests can be archived after completion

#### 3. User Management
* Create: Users can register for their own accounts
* Read: Retrieve user information for request tracking
* Authentication: Secure Login/Logout functionality for Users and Admins

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
* Session-based authentication for users and admin portal
* Password protection
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
| password | String(120) | Not Null         | User password                    |
| full_name| String(100) | Optional         | User's full name                 |

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

#### PickupRequest Table
| Field                | Type        | Constraints               | Description                 |
| -------------------- | ----------- | ------------------------- | --------------------------- |
| id                   | Integer     | Primary Key               | Unique request identifier   |
| user_id              | Integer     | Foreign Key (User.id)     | Requesting user             |
| item_description     | String(200) | Not Null                  | Description of e-waste item |
| item_type            | String(50)  | Default: Other            | Category of item            |
| status               | String(50)  | Default: Created          | Workflow status             |
| assigned_employee_id | Integer     | Foreign Key (Employee.id) | Assigned employee           |
| created_at           | DateTime    | Auto-generated            | Request creation timestamp  |

---

## API Reference

### Employee Endpoints
* **GET /api/employees**: Retrieve all employees.
* **POST /api/employees**: Create a new employee.
* **DELETE /api/employees/{emp_id}**: Delete an employee by ID.

### Pickup Request Endpoints
* **GET /api/requests**: Retrieve all pickup requests.
* **POST /api/requests**: Create a new pickup request.
* **PUT /api/requests/{req_id}/assign**: Assign a request to an employee.
* **PUT /api/requests/{req_id}/status**: Update the status of a pickup request.

### User Endpoints
* **GET /api/users/{user_id}**: Retrieve user information by ID.

---

## Installation and Setup

1. **Clone the repository** and navigate to the project directory.
2. **Create a Virtual Environment**:
   ```bash
   python -m venv myvenv
   # Windows
   myvenv\Scripts\activate
   # Mac/Linux
   source myvenv/bin/activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Initialize the database**: The application automatically creates `instance/database.db` on first run.
5. **Run the Flask application**:
   ```bash
   python app.py
   ```
   Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## Usage Guide

### Public User
1. **Register/Login**: Create an account from the Home Page.
2. **Dashboard**: Navigate to your personal Dashboard.
3. **Submit Request**: Click "New Request" to submit details about your e-waste.
4. **Track**: View the status of your requests in the "My Requests" table.

### Admin Portal
1. Login at `/admin/login` (Default: `admin` / `admin123`).
2. Manage Employees and Assign Requests.

### Employee Portal
1. Access the Employee Portal.
2. Select your name to view and update assigned tasks.

---

## Project Structure

```
e-waste-disposal-system/
├── app.py              # Main Flask application & Routes
├── models.py           # Database Models
├── instance/           # SQLite Database
├── static/             # Static files (CSS, JS)
├── templates/          # HTML Templates
│   ├── base.html       # Base layout
│   ├── index.html      # Landing Page
│   ├── user_dashboard.html # User Portal
│   ├── admin.html      # Admin Dashboard
│   └── ...
└── README.md           # Project Documentation
```

---

## Attribution

### Libraries and Frameworks
* **Flask**: Web framework for Python.
* **Flask-SQLAlchemy**: ORM extension for Flask.
* **SQLite**: Embedded relational database.

### Frontend Resources
* **HTML5/CSS3**: Markup and Styling.
* **Vanilla JavaScript**: Client-side interactivity.
* **Google Fonts**: 'Outfit' typeface.

---
*Developed for the DBS Programming for Information Systems Assessment.*
