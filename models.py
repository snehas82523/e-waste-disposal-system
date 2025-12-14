from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)  # In real app, hash this!

    def to_dict(self):
        return {
            'id': self.id, 
            'username': self.username, 
            'email': self.email
        }

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(50), default='Collector') # Collector, Driver, etc.
    status = db.Column(db.String(20), default='Active')
    start_date = db.Column(db.String(20)) # Storing as string for simplicity

    def to_dict(self):
        return {
            'id': self.id, 
            'name': self.name, 
            'email': self.email, 
            'phone': self.phone, 
            'role': self.role, 
            'status': self.status,
            'start_date': self.start_date
        }

class RecyclingCenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200))

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'location': self.location}

class PickupRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_description = db.Column(db.String(200), nullable=False)
    item_type = db.Column(db.String(50), nullable=False, default='Other')
    status = db.Column(db.String(50), default='Created') 
    # Statuses: Created, Assigned, Picked Up, Delivered to Center, Processed, Reward Collected, Delivered, Closed
    assigned_employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)
    assigned_center_id = db.Column(db.Integer, db.ForeignKey('recycling_center.id'), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    employee = db.relationship('Employee', backref='assignments')
    center = db.relationship('RecyclingCenter', backref='requests')
    user = db.relationship('User', backref='requests')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'item': self.item_description,
            'type': self.item_type,
            'status': self.status,
            'assigned_employee': self.employee.name if self.employee else None,
            'assigned_center': self.center.name if self.center else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
