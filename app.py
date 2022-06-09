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

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/mylist", methods=["GET"])
@login_required
def mylist():                
    if not db.execute("SELECT * FROM data_user WHERE id_user = ?", session["user_id"]):
        return render_template("mylist.html")
    
    else:
        diff_tables = db.execute("SELECT DISTINCT table_name FROM data_user WHERE id_user = ?", session["user_id"])
        data_list = []
        for row in diff_tables:
            data = db.execute("SELECT * FROM data_user WHERE id_user = ? and table_name = ?", session["user_id"], row["table_name"])
            data_dictionary = {"table_data": data,
                                "title": row["table_name"]} 

            data_list.append(data_dictionary)


        return render_template("mylist.html", data=data_list)

@app.route("/ranking")
def ranking():
    diff_tables = db.execute("SELECT DISTINCT table_name FROM data_user WHERE bool_ranking = 1")
    data_list = []
    for row in diff_tables:
        data_table = db.execute("SELECT * FROM data_user WHERE table_name = ?", row["table_name"])
        data_user = db.execute("SELECT * FROM users WHERE id = ?", data_table[0]["id_user"])
        data_dictionary = {"table_data": data_table,
                            "title": row["table_name"],
                            "owner": data_user[0]["user"]}

        data_list.append(data_dictionary)

    return render_template("ranking.html", data=data_list)

@app.route("/addlist", methods=["POST"])
@login_required
def addlist():
    if not request.form.get("content"):
            error = flash("You must put a comment")
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

        db.execute("INSERT INTO data_user (id_user, table_name, content, type, rate, comment, link) VALUES (?, ?, ?, ?, ?, ?, ?)", id, table_name, content, type, rate, comment, link)
        return redirect("/mylist")

@app.route("/deletelist")
@login_required
def deletelist():
    id_table = request.args.get("id_table", type=int)
    db.execute("DELETE FROM data_user WHERE content = ?", id_table)
    return redirect("/mylist")

@app.route("/toranking")
@login_required
def toranking():
    boolRanking = request.args.get("bool", type=int)

    if not db.execute("SELECT * FROM data_user WHERE id_user = ? AND bool_ranking = ?", session["user_id"], boolRanking):
        # Aqui será quando for 0
        db.execute("UPDATE data_user SET bool_ranking = 1 WHERE id_user = ?", session["user_id"])
        return redirect("/mylist")
    
    else:
        # Aqui será quando for 1
        db.execute("UPDATE data_user SET bool_ranking = 0 WHERE id_user = ?", session["user_id"])
        return redirect("/mylist")
