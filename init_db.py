from app import app
from models import db, User, Employee, PickupRequest

with app.app_context():
    db.drop_all()
    db.create_all()
    
    # Seed a demo user
    if not User.query.get(1):
        demo_user = User(username='DemoUser', email='user@example.com', password='password')
        db.session.add(demo_user)
        db.session.commit()
        print("Database initialized and Seed User created.")

    # Seed a demo Employee
    if not Employee.query.get(1):
        demo_emp = Employee(name='John Doe', email='john@example.com', role='collector', status='Active')
        db.session.add(demo_emp)
        print("Seed Employee created.")

    # Seed dummy Pickup Requests
    if not PickupRequest.query.get(1):
        req1 = PickupRequest(user_id=1, item_description='Old CRT Monitor', item_type='Monitor', status='Created')
        req2 = PickupRequest(user_id=1, item_description='Broken Microwave', item_type='Appliance', status='Assigned', assigned_employee_id=1)
        db.session.add(req1)
        db.session.add(req2)
        db.session.commit()
        print("2 Dummy Pickup Requests created.")
