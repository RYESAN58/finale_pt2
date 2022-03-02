from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.car import Car


@app.route('/make')
def report():
    x = session['user']
    y = session['name']
    return render_template('vehicle.html', x = x , name = y )

###################################################################################


@app.route('/add_site', methods = ['POST'])
def add():
    data = {
        'model' : request.form['model'],
        'make' : request.form['make'],
        'year' : request.form['year'],
        'description': request.form['description'],
        'User_id': request.form['User_id'],
        'price': request.form['price']
    }
    if not Car.validate(request.form):
        return redirect('/make')
    Car.create(data)
    num = session['user']
    return redirect(f'/dashboard/{num}')

###################################################################

@app.route('/see/<int:num>/<uname>')
def see(num, uname):
    data = {'id': num}
    y = Car.retrieve_by(data)
    name = session['name']
    x = session['user']

    return render_template("site.html", it = y, name = name, x = x, seller = uname)

################################################################################################

@app.route('/del/<int:num>')
def get_rid(num):
    data = {'id' : num}
    Car.delete(data)
    x = session['user']
    return redirect(f'/dashboard/{x}')


############################################################################################

@app.route('/edit/<int:num>')
def update(num):
    data = {'id' : num}
    edit = Car.retrieve_by(data)

    return render_template('update.html' , name =  session['name'], update = edit, x = session['user'], y = num)


@app.route('/update_rec', methods =['POST'])
def edit():
    data = {
        'model' : request.form['model'],
        'make' : request.form['make'],
        'year' : request.form['year'],
        'description': request.form['description'],
        'price': request.form['price'],
        'id':  request.form['id']
    }
    if not Car.validate(request.form):
        x = session['user']
        return redirect(f"/update/{request.form['id']}")
    Car.update(data)
    x = session['user']
    return redirect(f'dashboard/{x}')