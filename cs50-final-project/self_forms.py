from wtforms.validators import InputRequired, Length, EqualTo, Optional
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from flask_wtf import FlaskForm

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

class SearchForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=3, max=20)], render_kw={"placeholder": "Username"})
    submit = SubmitField("Search")

class MovieForm(FlaskForm):
    title = StringField(validators=[Optional()], render_kw={"placeholder": "Title"})
    genre = StringField(validators=[Optional()], render_kw={"placeholder": "Genre"})
    submit = SubmitField("Search")