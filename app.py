from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

DEFAULT_METRICS = {
    'critical_alerts': 0,
    'pending_requests': 0,
    'field_staff': 0,
    'open_centers': 0,
    'last_report_time': "Just Now",
    'recent_pickups': [] 
}

@app.route('/admin')
def admin_dashboard():
    return render_template('admin/index.html', 
        pickups=[], 
        employees=[], 
        centers=[], 
        reports=[],
        user_name='Admin User',  
        **DEFAULT_METRICS 
    )

@app.route('/admin/requests')
def admin_requests():
    return render_template('admin/requests.html', pickups=[])

@app.route('/admin/employees')
def admin_employees():
    return render_template('admin/employee.html', employees=[])

@app.route('/admin/centers')
def admin_centers():
    return render_template('admin/centers.html', centers=[])

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

@app.route('/admin/employees/register')
def admin_register_employee():
    return render_template('admin/employee_register.html')


if __name__ == '__main__':
    app.run(debug=True)