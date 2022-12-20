from flask import Flask, render_template, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.automap import automap_base
from self_forms import RegisterForm, LoginForm, BoardForm, SearchForm, MovieForm

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "secret_key"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

Base = automap_base()
Base.prepare(db.engine, reflect=True)
Board = Base.classes.board
Like = Base.classes.like
Movie = Base.classes.movie

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    share = db.Column(db.Boolean, default=True, unique=False)

@app.route("/", methods=['GET', 'POST'])
@login_required
def index():

    if request.method == "POST":
        id = request.form.get("id")
        if id:
            db.session.query(Like).filter_by(id=id).delete()
            db.session.commit()
            flash("Deletion was successful!")
            return redirect("/")

    boards = db.session.query(Like).filter_by(user=current_user.get_id(), what="Board").all()
    movies = db.session.query(Like).filter_by(user=current_user.get_id(), what="Movie").all()
    return render_template("index.html", boards=boards, movies=movies)

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
            else:
                flash("Invalid username and/or password!")
                redirect("/login")
        else:
            flash("Invalid username and/or password!")
            redirect("/login")

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

    if request.method == "POST":
        id = request.form.get("id")
        if id:
            game = db.session.query(Board).filter_by(id=id).first()
            players = f"{game.min_players} / {game.max_players}"
            new_entry = Like(user=current_user.get_id(), name=game.name, year=game.year,
                             what="Board", playtime=game.playtime, players=players)
            db.session.add(new_entry)
            db.session.commit()
            flash("Liking was successful!")
            return redirect("/")

    boards = 13
    return render_template("board.html", form=form, boards=boards)

@app.route("/movie", methods=['GET', 'POST'])
@login_required
def movie():

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

    if request.method == "POST":
        id = request.form.get("id")
        if id:
            movie = db.session.query(Movie).filter_by(id=id).first()
            new_entry = Like(user=current_user.get_id(), name=movie.title, year=movie.release,
                             what="Movie", playtime=movie.runtime, genre=movie.genre)
            db.session.add(new_entry)
            db.session.commit()
            flash("Liking was successful!")
            return redirect("/")

    movies = 13
    return render_template("movie.html", form=form, movies=movies)

@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():

    form = SearchForm()
    if form.validate_on_submit():
        name = form.username.data
        user = User.query.filter_by(username=name, share=True).first()
        if user:
            boards = db.session.query(Like).filter_by(user=user.id, what="Board").all()
            movies = db.session.query(Like).filter_by(user=user.id, what="Movie").all()
            if boards or movies:
                return render_template("search.html", boards=boards, form=form, username=name, movies=movies)
            else:
                flash("User doesn't have any favorites yet!")
                return redirect("/search")
        else:
            flash("Username doesn't exist or user doesn't want to share their favorites!")
            return redirect("/search")

    boards = 13
    return render_template("search.html", form=form, boards=boards)

@app.route("/setting", methods=["GET", "POST"])
@login_required
def setting():

    if request.method == "POST":
        share = int(request.form.get("share"))
        User.query.filter_by(id=current_user.get_id()).update({"share": share})
        db.session.commit()
        flash("Settings were saved successfully!")
        return redirect("/setting")

    user = User.query.filter_by(id=current_user.get_id()).first()
    return render_template("setting.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)