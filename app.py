from flask import Flask, render_template

# Initialize
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev_key'

# user page
@app.route('/')
def home():
    return render_template('index.html')

# admin login
@app.route('/admin/login')
def admin_login():
    return render_template('admin_login.html')  

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
