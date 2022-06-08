
from distutils.log import debug
from cs50 import SQL
from flask import render_template, redirect, Flask, request, flash, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
# Salvar informação que um usuário está conectado
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///shares.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    
    if request.method == "POST":
        if not request.form.get("username"):
            error = flash("Any username informed")
            return render_template("register.html", error=error)

        elif not request.form.get("password"):
            error = flash("Any password informed")
            return render_template("register.html", error=error)

        username = request.form.get("username").lower()
        data = db.execute("SELECT * FROM users WHERE user = ?", username)

        if len(data) != 1:
            error = flash("User doesn't exist")
            return render_template("login.html", error=error)

        elif not check_password_hash(data[0]["hash"], request.form.get("password")):
            error = flash("Password doesn't correspond")
            return render_template("login.html", error=error)

        else:
            session["user_id"] = data[0]["id"]
            return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = db.execute("SELECT * FROM users")
        if not request.form.get("username"):
            error = flash("Any username informed")
            return render_template("register.html", error=error)

        elif not request.form.get("password"):
            error = flash("Any password informed")
            return render_template("register.html", error=error)

        elif request.form.get("password") != request.form.get("confirmation"):
            error = flash("Passwords doesn't match")
            return render_template("register.html", error=error)

        name_low = request.form.get("username").lower()
        validation = db.execute("SELECT * FROM users WHERE user = ?", name_low)

        if len(validation) == 1:
            error = flash("Username already been used. Choose another one.")
            return render_template("register.html", error=error)

        else:
            pass_user = generate_password_hash(request.form.get("password"))
            name = request.form.get("username").lower()
            db.execute("INSERT INTO users (user, hash) VALUES (?, ?)", name, pass_user)
            return redirect("/login")


    else:
        return render_template("register.html")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        return render_template("other.html")

    else:
        return render_template("index.html")

@app.route("/mylist", methods=["GET", "POST"])
@login_required
def mylist():
    if request.method == "POST":
        if not request.form.get("content"):
            error = flash("Any content was fill")
            return render_template("mylist.html", error=error)

        elif len(request.form.get("comment")) > 240:
            error = flash("Comment section filled incorrectly")
            return render_template("mylist.html", error=error)

        else:
            if not request.form.get("rate"):
                rate = ""
            else:
                rate = float(request.form.get("rate"))
            
            table_name = request.form.get("table_name").lower()
            content = request.form.get("content").lower()
            type = request.form.get("type").lower()
            comment = request.form.get("comment").lower()
            link = request.form.get("link").lower()
            id = int(session["user_id"])

            db.execute("INSERT INTO tables (id, table_name, content, type, rate, comment, link) VALUES (?, ?, ?, ?, ?, ?, ?)", id, table_name, content, type, rate, comment, link)
            return redirect("/mylist")

        
    else:
        if not db.execute("SELECT * FROM tables WHERE id = ?", session["user_id"]):
            return render_template("mylist.html")
        
        else:
            geral = db.execute("SELECT * FROM tables WHERE id = ?", session["user_id"])
            diff_tables = db.execute("SELECT DISTINCT table_name FROM tables")
            data_list = []
            for row in diff_tables:
                data = db.execute("SELECT * FROM tables WHERE id = ? and table_name = ?", session["user_id"], row["table_name"])

                data_dictionary = {"table_data": data,
                                    "title": row["table_name"]} 

                data_list.append(data_dictionary)



            return render_template("mylist.html", data=data_list)

