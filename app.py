from flask import Flask, render_template,request, redirect, url_for, flash, session, jsonify
from models import db, Employee, PickupRequest

# Initialize
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# user page
@app.route('/')
def home():
    return render_template('index.html')

# admin login
# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid username or password")
            return redirect(url_for('admin_login'))
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))


# admin dashboard
@app.route('/admin')
def admin_dashboard():
    return render_template('admin.html')  

# employee
@app.route('/employee')
def employee_portal():
    return render_template('employee_portal.html')  

if __name__ == '__main__':
    app.run(debug=True)
