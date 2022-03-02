from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.car import Car

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    session['user'] = 0
    return render_template('index.html')
@app.route('/create_user', methods= ['POST'])
def created():


    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'firstname' : request.form['firstname'],
        'lastname' : request.form['lastname'],
        'email' : request.form['email'],
        'password': pw_hash
    }


    x = {'email':request.form['email']}
    checker = User.verify_email(x)
    if checker == False:
        return redirect('/')

    if not User.validate(request.form):
        return redirect('/')

    else:
        y = User.create(data)
        flash('Succesfully Added in database', 'success')
        return redirect('/')


########################################################################


@app.route('/login', methods = ['POST'])
def logger():
    data = {'email': request.form['email']}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password", 'login')
        return redirect("/")
    

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", 'login')
        return redirect('/')
    if len(request.form['password']) < 0:
        flash('must enter passoword')
        return redirect('/')
    session['user'] = user_in_db.id
    session['name'] = f"{user_in_db.firstname} {user_in_db.lastname}"
    x = session['user']
    return redirect(f'/dashboard/{x}')



@app.route('/dashboard/<int:num>/')
def home(num):
    if session['user'] != num:
        return redirect('/')
    x = num
    y = session['name']
    alls = Car.get_all_cars()
    return render_template('home.html',y= y, all = alls, id = x)