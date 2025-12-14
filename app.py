from flask import Flask, render_template,request, redirect, url_for, flash, session, jsonify
from models import db, Employee, PickupRequest
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

# user page
@app.route('/')
def home():
    return render_template('index.html')

# admin login
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



# admin dashboard
@app.route('/admin')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin.html')


# employee
@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([{"id": e.id, "name": e.name, "email": e.email, "phone": e.phone} for e in employees])

# Add employee
@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    new_emp = Employee(name=data['name'], email=data['email'], phone=data.get('phone'))
    db.session.add(new_emp)
    db.session.commit()
    return jsonify({"message": "Employee added", "id": new_emp.id})


# Submit pickup request from home page
@app.route('/pickup', methods=['POST'])
def create_request():
    data = request.get_json()
    new_request = PickupRequest(item_type=data['item_type'], description=data['description'])
    db.session.add(new_request)
    db.session.commit()
    return jsonify({"message": "Pickup request submitted", "id": new_request.id})

# Get all pickup requests (for admin)
@app.route('/pickup', methods=['GET'])
def get_requests():
    requests = PickupRequest.query.order_by(PickupRequest.created_at.desc()).all()
    return jsonify([{
        "id": r.id, "item_type": r.item_type, "description": r.description, "status": r.status
    } for r in requests])


if __name__ == '__main__':
    app.run(debug=True)
