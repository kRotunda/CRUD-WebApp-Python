import flask
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required


app = Flask(__name__, static_url_path="/static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '~~qwertyuiop!!'
login_manager = LoginManager(app)
login_manager.init_app(app)
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    cars = db.relationship('Car', backref='user')

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(20), nullable=False)
    model = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(20), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))

from app import db, User, Car
db.create_all()

@login_manager.user_loader
def load_user(uid):
    return User.query.get(uid)

@app.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('home.html', lCheck = 1)
    else:
        return render_template('home.html')

@app.route('/create', methods=['GET','POST'])
def create():
    if current_user.is_authenticated:
        if request.method == 'POST':
            make = request.form['make']
            model = request.form['model']
            year = request.form['year']
            color = request.form['color']
            newCar = Car(make=make, model=model, year=year, color=color, userId=current_user.id)
            db.session.add(newCar)
            db.session.commit()
            return render_template('create.html', lCheck=1, mCheck=1)
        return render_template('create.html', lCheck=1)
    else:
        if request.method == 'POST':
            un = request.form['username']
            pw = request.form['password']
            n = request.form['name']
            a = request.form['age']
            newUser = User(username=un, password=pw, name=n, age=a)
            user = User.query.filter_by(username=un).first()
            if user != None:
                return render_template('create.html', uCheck=un)
            db.session.add(newUser)
            db.session.commit()
            user = User.query.filter_by(username=un).first()
            login_user(user)
            return flask.redirect("/")
    return render_template('create.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        un = request.form['username']
        p = request.form['password']
        user = User.query.filter_by(username=un).first()
        if user == None:
            return render_template('login.html', err=1)
        else:
            if (user.password == p):
                login_user(user)
                return flask.redirect('/')
            else:
                return render_template('login.html', err=1)
    return render_template('login.html')

@app.route('/view_all')
@login_required
def viewAll():
    results = User.query.all()
    resultsCar = Car.query.filter_by(userId=current_user.id)
    resultsAllCar = Car.query.all()
    return render_template('view.html', users=results, lCheck=1, cars=resultsCar, allCar=resultsAllCar)

@app.route('/update', methods=['GET','POST'])
@login_required
def update():
    if request.method == 'POST':
        op = request.form['oldPassword']
        if current_user.password != op:
            return render_template('update.html', pCheck=op, lCheck = 1)
        upUser = User.query.filter_by(id=current_user.id).first()
        upUser.password = request.form['newPassword']
        db.session.commit()
        return flask.redirect('/')
    return render_template('update.html', lCheck = 1)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return flask.redirect("/")

@app.route('/delete/<id>', methods=['GET','POST'])
@login_required
def delete(id):
    if request.method == 'POST':
        delCar = Car.query.filter_by(id=id).first()
        db.session.delete(delCar)
        db.session.commit()
        return flask.redirect("/view_all")
    return flask.redirect("/view_all")

@app.route('/update/<id>', methods=['GET','POST'])
@login_required
def updateCar(id):
    if request.method == 'POST':
        upCar = Car.query.filter_by(id=id).first()
        upCar.make=request.form['make']
        upCar.model=request.form['model']
        upCar.year=request.form['year']
        upCar.color=request.form['color']
        db.session.commit()
        return flask.redirect("/view_all")
    car = Car.query.filter_by(id=id).first()
    return render_template('create.html', lCheck=1, updateCar=1, id=id, make=car.make, model=car.model, year=car.year, color=car.color)

@app.errorhandler(404)
def err404(err):
    if current_user.is_authenticated:
        return render_template('404.html', err=err, lCheck = 1)
    else:
        return render_template('404.html', err=err)

if __name__ == "__main__":
    app.run(debug=True)