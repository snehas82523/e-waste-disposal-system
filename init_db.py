from app import app
from models import db, User

with app.app_context():
    db.drop_all()
    db.create_all()
    
    # Seed a demo user
    if not User.query.get(1):
        demo_user = User(username='DemoUser', email='user@example.com', password='password')
        db.session.add(demo_user)
        db.session.commit()
        print("Database initialized and Seed User created.")
