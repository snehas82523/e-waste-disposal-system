from app import app, db
from models import Employee, Pickup , RecyclingCenter

with app.app_context():
    db.create_all()
    

    Employee.query.delete()
    Pickup.query.delete()
    
    #  dummy employees
    emp1 = Employee(name="Alice Johnson", email="alice@example.com", phone="1234567890", password="pass123")
    emp2 = Employee(name="Bob Smith", email="bob@example.com", phone="0987654321", password="pass456")
    db.session.add_all([emp1, emp2])

    #dummy centers 
    center1 = RecyclingCenter(name="Eco-Recycle", location="North Zone", capacity=500)
    center2 = RecyclingCenter(name="Green Tech", location="South Zone", capacity=800)
    db.session.add_all([center1, center2])
    
    # dummy pickups
    pickup1 = Pickup(user_name="John Doe", item_description="Old Laptop", status="Pending")
    pickup2 = Pickup(user_name="Jane Roe", item_description="Broken Monitor", status="Assigned")
    db.session.add_all([pickup1, pickup2])
    
    db.session.commit()
    
    print("Database populated with dummy data!")
