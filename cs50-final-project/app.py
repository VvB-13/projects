from flask import Flask, render_template, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length, EqualTo, Optional
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.automap import automap_base

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "secret_key"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

Base = automap_base()
Base.prepare(db.engine, reflect=True)
Board = Base.classes.board
Likes = Base.classes.likes

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=3, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=3, max=20), EqualTo("password_confirm"),], render_kw={"placeholder": "Password"})
    password_confirm = PasswordField(validators=[InputRequired(), Length(
        min=3, max=20)], render_kw={"placeholder": "Password (again)"})
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=3, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=3, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

class BoardForm(FlaskForm):
    name = StringField(validators=[Optional()], render_kw={"placeholder": "Name"})
    year = IntegerField(validators=[Optional()], render_kw={"placeholder": "Year"})
    submit = SubmitField("Search")

@app.route("/")
@login_required
def index():
    likes = db.session.query(Likes).filter_by(user=current_user.get_id()).all()
    return render_template("index.html", likes=likes)

@app.route("/register", methods=['GET', 'POST'])
def register():

    form = RegisterForm()
    if form.validate_on_submit():
        existing_username = User.query.filter_by(username=form.username.data).first()
        if existing_username:
            flash("Username already exists!")
            return redirect("/register")
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user)
        flash("You were successfully registerd!")
        return redirect("/")

    return render_template("register.html", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You were successfully logged in!")
                return redirect("/")

    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were successfully logged out!")
    return redirect("/login")

@app.route("/board", methods=['GET', 'POST'])
@login_required
def board():

    form = BoardForm()
    if form.validate_on_submit():
        name = form.name.data
        year = form.year.data
        if name and not year:
            games = db.session.query(Board).filter(Board.name.contains(name)).limit(10)
        elif year and not name:
            games = db.session.query(Board).filter_by(year=year).limit(10)
        elif name and year:
            games = db.session.query(Board).filter(Board.name.contains(name), year == Board.year).limit(10)
        else:
            flash("You need to input at least one field!")
            return redirect("/board")
        return render_template("board.html", games=games, form=form)

    if request.method == "POST":
        id = request.form.get("id")
        if id:
            game = db.session.query(Board).filter_by(id=id).first()
            players = f"{game.min_players} / {game.max_players}"
            new_entry = Likes(user=current_user.get_id(), name=game.name, year=game.year,
                             what="Board", playtime=game.playtime, players=players)
            db.session.add(new_entry)
            db.session.commit()
            flash("Liking was successful!")
            return redirect("/")

    games = 13
    return render_template("board.html", form=form, games=games)