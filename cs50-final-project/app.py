from flask import Flask, render_template, redirect
from cs50 import SQL
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQL("sqlite:///operations_research.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/tsp")
def tsp():
    return render_template("tsp.html")

@app.route("/knapsack")
def knapsack():
    return render_template("knapsack.html")

@app.route("/logout")
def logout():
    return redirect("/")