E-Waste Disposal and Reward System
Overview

The E-Waste Disposal and Reward System is a web-based platform designed to streamline the collection, tracking, and processing of electronic waste. It replaces manual coordination with a centralized digital system where users can request e-waste pickup, administrators can assign tasks, and employees can update collection and processing status.

To encourage responsible disposal, users are rewarded for their efforts with eco-friendly products such as keychains, pen holders, and phone covers made from recycled e-waste materials. The system ensures transparency, operational efficiency, and proper lifecycle management of electronic waste.

Technologies Used

    Backend: Python, Flask
    Frontend: HTML5, CSS3, JavaScript (Fetch API)
    Database: SQLite, SQLAlchemy ORM
    Architecture: RESTful API (Single Page Application)
    Version Control: Git, GitHub
    Deployment: PythonAnywhere

Features

Role-based Access:

    Admin – full control over employees and pickup requests

    User – submit and track e-waste pickup requests

    Employee – manage assigned pickup tasks

CRUD Operations:

    Employees, Users, and Pickup Requests

Request Workflow Management:

    Created → Assigned → Picked Up → Delivered → Processed → Closed

Real-time Tracking:

    Users can monitor request status through their dashboard

Validation & Data Integrity:

    Input validation on frontend and backend

    Foreign key constraints and unique email enforcement

API-Driven System:

    Asynchronous communication using Fetch API for smooth user experience

Responsive UI:

    Clean, modern, eco-friendly interface usable on desktop and mobile devices

Useful Commands:

Setup & Run Project:

      Create virtual environment:  python -m venv myvenv


      Activate environment (Windows): myvenv\Scripts\activate


      Install dependencies: pip install -r requirements.txt


      Run the Flask app:python app.py

      Open in browser: http://127.0.0.1:5000

Project Structure:  

e-waste-disposal-system/
|-- app.py              # Main Flask application & routes
|--models.py           # Database models
| instance/           # SQLite database
|-- static/             # CSS and JavaScript files
|-- templates/          # HTML templates
|-- requirements.txt    # Dependencies
|-- README.md           # Project documentation

Live Demo:https://sneha2025.pythonanywhere.com/

Conclusion

The E-Waste Disposal and Reward System provides an efficient and scalable solution for managing electronic waste recycling. By digitizing pickup requests, employee assignment, and workflow tracking, the system reduces manual effort, improves accountability, and enhances environmental sustainability. Its role-based access, RESTful architecture, and user-friendly interface make it a reliable platform for modern e-waste management.

References

      Flask Documentation: https://flask.palletsprojects.com/

      Flask SQLAlchemy: https://flask-sqlalchemy.palletsprojects.com/

      YouTube Tutorial: https://www.youtube.com/watch?v=SSqvwa2bx5k

      https://blog.miguelgrinberg.com/

      https://chatgpt.com/share/693e2d91-1850-800b-8945-b554a4db13d0

      https://chatgpt.com/share/693e259c-49ac-800b-9faf-87387044c622

      https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch

      https://thepythoncode.com/article/building-crud-app-with-flask-and-sqlalchemy

      https://chatgpt.com/share/6940679e-0ae8-800b-9c47-4ac14bcee9a9

      https://chatgpt.com/share/693d9fe7-6d18-800b-b260-a69ba6aac57f

      https://chatgpt.com/share/693d9abc-2910-800b-991e-7f3320b250a7

      https://chatgpt.com/share/693d9078-f950-800b-8f60-eacf3671b512

      https://developer.mozilla.org/en-US/docs/Web/API/Document/DOMContentLoaded_event

      https://chatgpt.com/share/693d7a94-50b8-800b-8cd5-a8a63ab64379

      https://chatgpt.com/share/693b72cc-7d80-800b-a383-cf13d77b74de

      https://chatgpt.com/share/693b3dff-5f4c-800b-a469-ffbdaf8e08c7
