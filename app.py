from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from models import db, User, Employee, PickupRequest
import os

# Initialize
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'dev_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# --- User Pages ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Hardcoded Admin Credentials
        if username == 'admin' and password == 'admin123':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials')
            return redirect(url_for('admin_login'))
            
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('home'))

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin.html')

# --- Employee APIs ---
@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([{"id": e.id, "name": e.name, "email": e.email, "phone": e.phone} for e in employees])

@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    new_emp = Employee(name=data['name'], email=data['email'], phone=data.get('phone'))
    db.session.add(new_emp)
    db.session.commit()
    return jsonify({"message": "Employee added", "id": new_emp.id})

@app.route('/api/employees', methods=['GET'])
def get_employees_api():
    employees = Employee.query.all()
    return jsonify([e.to_dict() for e in employees])

@app.route('/api/employees', methods=['POST'])
def create_employee():
    data = request.json
    new_employee = Employee(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone'),
        role=data.get('role', 'Collector'),
        status='Active',
        start_date=data.get('start_date')
    )
    db.session.add(new_employee)
    try:
        db.session.commit()
        return jsonify(new_employee.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/employees/<int:emp_id>', methods=['DELETE'])
def delete_employee(emp_id):
    emp = Employee.query.get_or_404(emp_id)
    try:
        db.session.delete(emp)
        db.session.commit()
        return jsonify({'message': 'Employee deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# --- Pickup Requests ---
@app.route('/api/requests', methods=['POST'])
def create_request():
    data = request.json
    # Assume User ID 1 exists for demo if not provided
    user_id = data.get('user_id', 1)
    
    # Create demo user if missing
    if user_id == 1 and not User.query.get(1):
        demo_user = User(id=1, username='DemoUser', email='user@example.com', password='password')
        db.session.add(demo_user)
        db.session.commit()

    new_req = PickupRequest(
        user_id=user_id,
        item_description=data['item_description'],
        item_type=data.get('item_type', 'Other')
    )
    db.session.add(new_req)
    db.session.commit()
    return jsonify(new_req.to_dict()), 201

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@app.route('/pickup', methods=['POST'])
def create_pickup_request():
    data = request.get_json()
    new_request = PickupRequest(item_type=data['item_type'], description=data['description'])
    db.session.add(new_request)
    db.session.commit()
    return jsonify({"message": "Pickup request submitted", "id": new_request.id})

@app.route('/pickup', methods=['GET'])
def get_requests():
    requests = PickupRequest.query.order_by(PickupRequest.created_at.desc()).all()
    return jsonify([{
        "id": r.id, "item_type": r.item_type, "description": r.description, "status": r.status
    } for r in requests])

# --- New Routes for Assignment & Status ---
@app.route('/api/requests/<int:req_id>/assign', methods=['PUT'])
def assign_request(req_id):
    data = request.json
    req = PickupRequest.query.get_or_404(req_id)
    
    if 'employee_id' in data:
        req.assigned_employee_id = data['employee_id']
        req.status = 'Assigned'
    
    if 'center_id' in data:
        req.assigned_center_id = data['center_id']
    
    db.session.commit()
    return jsonify(req.to_dict())

@app.route('/api/requests/<int:req_id>/status', methods=['PUT'])
def update_request_status(req_id):
    data = request.json
    req = PickupRequest.query.get_or_404(req_id)
    
    if 'status' in data:
        req.status = data['status']
    
    db.session.commit()
    return jsonify(req.to_dict())

if __name__ == '__main__':
    app.run(debug=True)
