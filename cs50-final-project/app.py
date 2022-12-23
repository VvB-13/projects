from flask import Flask, render_template, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.automap import automap_base
from self_forms import RegisterForm, LoginForm, BoardForm, SearchForm, MovieForm

# Initialisng Flask, bcrypt and SQLalchemy
app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "secret_key"

# Setup LoginManager flask_login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Setup automap for database classes
Base = automap_base()
Base.prepare(db.engine, reflect=True)
Board = Base.classes.board
Like = Base.classes.like
Movie = Base.classes.movie
Game = Base.classes.game

# Loginmanager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User class for db and UserMixin
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    share = db.Column(db.Boolean, default=True, unique=False)

@app.route("/", methods=['GET', 'POST'])
@login_required
def index():

    # Delete Option
    if request.method == "POST":
        id = request.form.get("id")
        if id:
            db.session.query(Like).filter_by(id=id).delete()
            db.session.commit()
            flash("Delete was successful!")
            return redirect("/")

    # Displaying likes of boards, movies and games
    boards = db.session.query(Like).filter_by(user=current_user.get_id(), what="Board").all()
    movies = db.session.query(Like).filter_by(user=current_user.get_id(), what="Movie").all()
    games = db.session.query(Like).filter_by(user=current_user.get_id(), what="Game").all()
    return render_template("index.html", boards=boards, movies=movies, games=games)

@app.route("/register", methods=['GET', 'POST'])
def register():

    # Form on submit: Checking if username exists
    # adding user with hashed password to the database
    # Logging user in
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

    # Template with form
    return render_template("register.html", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    
    # login form submit checking password and logging in, otherwise flashing message
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You were successfully logged in!")
                return redirect("/")
            else:
                flash("Invalid username and/or password!")
                redirect("/login")
        else:
            flash("Invalid username and/or password!")
            redirect("/login")

    # Render page with form
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    # Logout plus flash
    logout_user()
    flash("You were successfully logged out!")
    return redirect("/login")

@app.route("/board", methods=['GET', 'POST'])
@login_required
def board():

    # form for board game search; either name or year for search (otherwise flash)
    # querying for boards if valide search; Rendering with results
    form = BoardForm()
    if form.validate_on_submit():
        name = form.name.data
        year = form.year.data

        if name and not year:
            boards = db.session.query(Board).filter(Board.name.contains(name)).limit(10).all()
        elif year and not name:
            boards = db.session.query(Board).filter_by(year=year).limit(10).all()
        elif name and year:
            boards = db.session.query(Board).filter(Board.name.contains(name), year == Board.year).limit(10).all()
        else:
            flash("You need to input at least one field!")
            return redirect("/board")

        if boards:
            return render_template("board.html", boards=boards, form=form)
        else:
            flash("No Board Game found for the given search!")
            return redirect("/board")

    # Like of searched board games
    # Adding to db; flash
    if request.method == "POST":
        id = request.form.get("id")
        if id:
            game = db.session.query(Board).filter_by(id=id).first()
            players = f"{game.min_players} / {game.max_players}"
            new_entry = Like(user=current_user.get_id(), name=game.name, year=game.year,
                             what="Board", playtime=game.playtime, players=players)
            db.session.add(new_entry)
            db.session.commit()
            flash("Like was successful!")
            return redirect("/")

    # Render page with form
    boards = 13
    return render_template("board.html", form=form, boards=boards)

@app.route("/movie", methods=['GET', 'POST'])
@login_required
def movie():

    # form for movie search; either title or genre for search (otherwise flash)
    # querying for movies if valide search; Rendering with results    
    form = MovieForm()
    if form.validate_on_submit():
        title = form.title.data
        genre = form.genre.data

        if title and not genre:
            movies = db.session.query(Movie).filter(Movie.title.contains(title)).limit(10).all()
        elif genre and not title:
            movies = db.session.query(Movie).filter(Movie.genre.contains(genre)).limit(10).all()
        elif title and genre:
            movies = db.session.query(Movie).filter(Movie.title.contains(title), Movie.genre.contains(genre)).limit(10).all()
        else:
            flash("You need to input at least one field!")
            return redirect("/movie")

        if movies:
            return render_template("movie.html", movies=movies, form=form)
        else:
            flash("No Movie found for the given search!")
            return redirect("/movie")

    # Like of searched movies
    # Adding to db; flash
    if request.method == "POST":
        id = request.form.get("id")
        if id:
            movie = db.session.query(Movie).filter_by(id=id).first()
            new_entry = Like(user=current_user.get_id(), name=movie.title, year=movie.release,
                             what="Movie", playtime=movie.runtime, genre=movie.genre)
            db.session.add(new_entry)
            db.session.commit()
            flash("Like was successful!")
            return redirect("/")

    # Render page with form
    movies = 13
    return render_template("movie.html", form=form, movies=movies)

@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():

    # Searching for user via SearchForm; Checking if share setting is on
    # displaying boards, movies and games of user
    # Otherwise flash (eg setting off)
    form = SearchForm()
    if form.validate_on_submit():
        name = form.username.data
        user = User.query.filter_by(username=name, share=True).first()
        if user:
            boards = db.session.query(Like).filter_by(user=user.id, what="Board").all()
            movies = db.session.query(Like).filter_by(user=user.id, what="Movie").all()
            games = db.session.query(Like).filter_by(user=user.id, what="Game").all()
            if boards or movies or games:
                return render_template("search.html", boards=boards, form=form, username=name, movies=movies, games=games)
            else:
                flash("User doesn't have any favorites yet!")
                return redirect("/search")
        else:
            flash("Username doesn't exist or user doesn't want to share their favorites!")
            return redirect("/search")

    # Render page with form
    boards = 13
    return render_template("search.html", form=form, boards=boards)

@app.route("/setting", methods=["GET", "POST"])
@login_required
def setting():

    # Setting for share function
    # if changed then changed in the db
    if request.method == "POST":
        share = int(request.form.get("share"))
        User.query.filter_by(id=current_user.get_id()).update({"share": share})
        db.session.commit()
        flash("Settings were saved successfully!")
        return redirect("/setting")

    # Render page depending on the existing setting
    user = User.query.filter_by(id=current_user.get_id()).first()
    return render_template("setting.html", user=user)

@app.route("/game", methods=['GET', 'POST'])
@login_required
def game():

    # form for game search; either title or genre for search (otherwise flash)
    # querying for games if valide search; Rendering with results
    form = MovieForm()
    if form.validate_on_submit():
        title = form.title.data
        genre = form.genre.data

        if title and not genre:
            games = db.session.query(Game).filter(Game.title.contains(title)).limit(10).all()
        elif genre and not title:
            games = db.session.query(Game).filter(Game.genre.contains(genre)).limit(10).all()
        elif title and genre:
            games = db.session.query(Game).filter(Game.title.contains(title), Game.genre.contains(genre)).limit(10).all()
        else:
            flash("You need to input at least one field!")
            return redirect("/game")

        if games:
            return render_template("game.html", games=games, form=form)
        else:
            flash("No Game found for the given search!")
            return redirect("/game")

    # Like of searched games
    # Adding to db; flash
    if request.method == "POST":
        id = request.form.get("id")
        if id:
            game = db.session.query(Game).filter_by(id=id).first()
            new_entry = Like(user=current_user.get_id(), name=game.title, year=game.release,
                             what="Game", developer=game.runtime, genre=game.genre)
            db.session.add(new_entry)
            db.session.commit()
            flash("Like was successful!")
            return redirect("/")

    # Render page with form
    games = 13
    return render_template("game.html", form=form, games=games)

# app reloades automatically and displaying debugging in browser
if __name__ == "__main__":
    app.run(debug=True)