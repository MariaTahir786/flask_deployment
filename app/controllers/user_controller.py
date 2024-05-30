from app import app
from app.models.user_model import User
from flask import Flask, render_template, request,session,redirect, flash
from flask_bcrypt import Bcrypt
from app.models.chore_model import Chores
from app.models.user_model import User

bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('/user/home.html')

@app.route('/user/register', methods = ["POST"])
def register():

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email_address": request.form['email_address'],
        "password": request.form['password'],
    }

    if User.validate_registration(request.form):
        User.register(data)
        return redirect('/')
    return redirect('/')

@app.route('/user/login', methods = ['POST'])
def login():
    form = request.form

    user = User.get_by_email(form.get('email_address'))

    if not user or not bcrypt.check_password_hash(user.password, request.form['password']):

        flash("Invalid Credentials", 'login')
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/user/dashboard')


@app.route('/user/dashboard')
def dashboard():

    if not 'user_id' in session:
        return redirect('/')

    return render_template('/user/dashboard.html', chores = Chores.get_all_chores())


@app.route('/user/logout')
def logout():
    session.clear()
    return redirect('/')
