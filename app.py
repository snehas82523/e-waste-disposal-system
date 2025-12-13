from flask import Flask, render_template

# Initialize
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev_key'

@app.route('/')
def home():
    return "<h1>Hello! The E-Waste System is Running.</h1>"

if __name__ == '__main__':
    app.run(debug=True)
