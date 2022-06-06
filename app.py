from cs50 import SQL
from flask import render_template, redirect, Flask, request, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
# Salvar informação que um usuário está conectado
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///shares.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = db.execute("SELECT * FROM users")
        validation = (db.execute("SELECT * FROM users WHERE user = ?"), request.form.get("username").lower())
        if not request.form.get("username"):
            error = flash("Any username informed")
            return render_template("register.html", error=error)

        elif not request.form.get("password"):
            error = flash("Any password informed")
            return render_template("register.html", error=error)

        elif request.form.get("password") != request.form.get("confirmation"):
            error = flash("Passwords doesn't match")
            return render_template("register.html", error=error)

        elif len(validation[0]["user"]) == 1:
            error = flash("Username already been used. Choose another one.")
            return render_template("register.html", error=error)

        else:
            pass_user = generate_password_hash(request.form.get("password"))
            name = request.form.get("username").lower()
            db.execute("INSERT INTO users (user, hash) VALUES (?, ?)", name, pass_user)
            return redirect("/login")


    else:
        return render_template("register.html")