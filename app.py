from flask import Flask, render_template, redirect, url_for,request
from models import db, Employee, Pickup,RecyclingCenter
import os


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/admin')
def admin_dashboard():
    pickups = Pickup.query.all()
    employees = Employee.query.all()
    centers = RecyclingCenter.query.all()
    reports = []  


    for pickup in pickups:
        if pickup.status.upper() == 'ASSIGNED' and not pickup.assigned_employee_id:
            pickup.display_status = 'PENDING'
        elif pickup.status.upper() == 'ASSIGNED' and pickup.assigned_employee_id:
            pickup.display_status = 'ASSIGNED'
        elif pickup.status:
            pickup.display_status = pickup.status.upper()
        else:
            pickup.display_status = 'PENDING'

    DEFAULT_METRICS = {
        'critical_alerts': 0,
        'pending_requests': len([p for p in pickups if p.status.lower() == 'pending']),
        'field_staff': len(employees),
        'open_centers': 0,
        'last_report_time': "Just Now",
        'recent_pickups': pickups[::-1][-5:]  
    }


    return render_template(
        'admin/index.html',
        pickups=pickups,
        employees=employees,
        centers=centers,
        reports=reports,
        user_name='Admin User',
        **DEFAULT_METRICS
    )



@app.route('/admin/requests')
def admin_requests():
    pickups = Pickup.query.all()
    employees = Employee.query.all()  
    centers = RecyclingCenter.query.all()

    for pickup in pickups:
        pickup.assigned_employee_name = pickup.assigned_employee.name if pickup.assigned_employee else 'Unassigned'
        pickup.assigned_center_name = pickup.assigned_center_obj.name if pickup.assigned_center_obj else 'Pending'
    return render_template('admin/requests.html', pickups=pickups, employees=employees, centers=centers)




@app.route('/admin/employees')
def admin_employees():
    employees = Employee.query.all()  
    return render_template('admin/employee.html', employees=employees)



@app.route('/admin/centers')
def admin_centers():
    centers = RecyclingCenter.query.all()
    return render_template('admin/centers.html', centers=centers)


@app.route('/admin/reports')
def admin_reports():
    return render_template('admin/reports.html', reports=[])


@app.route('/admin/settings')
def admin_settings():
    user_data = {
        'username': 'Admin User',
        'email': 'admin@ewaste.com',
        'last_login': '2025-11-23 20:36:00',
        'role': 'System Administrator'
    }
    return render_template('admin/settings.html', user=user_data)



@app.route('/logout')
def logout():
    return redirect(url_for('admin_dashboard'))



@app.route('/admin/employees/register', methods=['GET', 'POST'])
def admin_register_employee():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        new_employee = Employee(name=name,  phone=phone,email=email, password=password )
        db.session.add(new_employee)
        db.session.commit()

        print(f"New employee added: {name}, {phone},{password},{email}")
        return redirect(url_for('admin_employees'))

    return render_template('admin/employee_register.html')



@app.route('/admin/requests/<int:pickup_id>/assign', methods=['POST'])
def assign_employee(pickup_id):
    employee_id = request.form.get('employee_id')
    pickup = Pickup.query.get_or_404(pickup_id)
    center_id_str = request.form.get('center_id')

    employee_id = int(employee_id_str) if employee_id_str and employee_id_str != 'None' else None
    center_id = int(center_id_str) if center_id_str and center_id_str != 'None' else None

    if employee_id and employee_id != 'None':
        pickup.assigned_employee_id = employee_id
        pickup.status = 'Assigned'
    else:
        pickup.assigned_employee_id = None
        pickup.status = 'Pending' 
    
    db.session.commit()
    return redirect(url_for('admin_requests'))


@app.route('/admin/requests/<int:id>')
def view_pickup(id):
    pickup = Pickup.query.get_or_404(id)
    return render_template('admin/view_pickup.html', pickup=pickup)


if __name__ == '__main__':
    app.run(debug=True)
