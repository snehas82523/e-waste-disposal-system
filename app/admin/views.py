from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

admin = Blueprint('admin', __name__)

@admin.route('/')
@login_required
def index():
    """Admin dashboard"""
    return render_template('admin/index.html')


@admin.route('/login')
def login():
    return render_template('admin/login.html', title="Admin Login")