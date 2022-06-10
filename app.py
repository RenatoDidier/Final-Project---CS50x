from cs50 import SQL
from flask import render_template, redirect, Flask, request, flash, session
from flask_session import Session
from sqlalchemy import table
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
            return render_template("login.html", error=error)

        elif not request.form.get("password"):
            error = flash("Any password informed")
            return render_template("login.html", error=error)

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
            error = flash("no")
            error = flash("You account was created!")
            return render_template("login.html", error=error)


    else:
        return render_template("register.html")

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/mylist")
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
                                "title": row["table_name"],
                                "active": data[0]["bool_ranking"]} 

            data_list.append(data_dictionary)


        return render_template("mylist.html", data=data_list)

@app.route("/ranking")
def ranking():
    diff_tables = db.execute("SELECT DISTINCT table_name FROM data_user WHERE bool_ranking = 1")
    data_list = []
    for row in diff_tables:
        data_table = db.execute("SELECT * FROM data_user WHERE table_name = ?", row["table_name"])
        data_user = db.execute("SELECT * FROM users WHERE id = ?", data_table[0]["id_user"])
        
        if not db.execute("SELECT * FROM vote_table WHERE id_owner = ? AND table_name = ?", data_table[0]["id_user"], data_table[0]["table_name"]):
            data_vote = [{"upvote": 0, "downvote": 0}]
        else:
            data_vote =  db.execute("SELECT * FROM vote_table WHERE id_owner = ? AND table_name = ?", data_table[0]["id_user"], data_table[0]["table_name"])
        
        data_dictionary = {"table_data": data_table,
                            "title": row["table_name"],
                            "owner": data_user[0]["user"],
                            "id": data_user[0]["id"],
                            "upvote": data_vote[0]["upvote"],
                            "downvote": data_vote[0]["downvote"]}

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
    db.execute("DELETE FROM data_user WHERE id_table = ?", id_table)
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

@app.route("/voteSystem")
@login_required
def voteSystem(): 
    action = request.args.get("action", type=int)
    owner_id = request.args.get("owner_id", type=int)
    table_name = request.args.get("table_name", type=str)
    if not db.execute("SELECT * FROM vote_check WHERE id_owner = ? AND table_name = ? AND voter_id = ?", owner_id, table_name, session["user_id"]):
        db.execute("INSERT INTO vote_check (id_owner, table_name, action, voter_id) VALUES (?, ?, ?, ?)", owner_id, table_name, action, session["user_id"])
        if action == 1:
            if not db.execute("SELECT * FROM vote_table WHERE id_owner = ? AND table_name = ?", owner_id, table_name):
                db.execute("INSERT INTO vote_table (id_owner, table_name, upvote, downvote) VALUES (?, ?, ?, 0)", owner_id, table_name, action)
                return redirect("/ranking")
            else:
                data = db.execute("SELECT * FROM vote_table WHERE id_owner = ? AND table_name = ?", owner_id, table_name)
                sum = data[0]["upvote"] + action
                db.execute("UPDATE vote_table SET upvote = ? WHERE id_owner = ? AND table_name = ?", sum, owner_id, table_name)
                return redirect("/ranking")

        else:
            if not db.execute("SELECT * FROM vote_table WHERE id_owner = ? AND table_name = ?", owner_id, table_name):
                action = -action
                db.execute("INSERT INTO vote_table (id_owner, table_name, upvote, downvote) VALUES (?, ?, 0, ?)", owner_id, table_name, action)
                return redirect("/ranking")
            else:
                data = db.execute("SELECT * FROM vote_table WHERE id_owner = ? AND table_name = ?", owner_id, table_name)
                sum = data[0]["downvote"] - action
                db.execute("UPDATE vote_table SET downvote = ? WHERE id_owner = ? AND table_name = ?", sum, owner_id, table_name)
                return redirect("/ranking")

    
    else:
        if action == 1:
            data = db.execute("SELECT * FROM vote_check WHERE id_owner = ? AND table_name = ? AND voter_id = ?", owner_id, table_name, session["user_id"])
            if data[0]["action"] == 1 or data[0]["action"] == 2:
                if data[0]["action"] == 1:
                    db.execute("UPDATE vote_check SET action = 0 WHERE id_owner = ? AND table_name = ? AND voter_id = ?", owner_id, table_name, session["user_id"])
                else:
                    db.execute("UPDATE vote_check SET action = -1 WHERE id_owner = ? AND table_name = ? AND voter_id = ?", owner_id, table_name, session["user_id"])

                data_vote_table = db.execute("SELECT * FROM vote_table WHERE id_owner = ? AND table_name = ?", owner_id, table_name)
                sum_upvote = data_vote_table[0]["upvote"] - action
                db.execute("UPDATE vote_table SET upvote = ? WHERE id_owner = ? AND table_name = ?", sum_upvote, owner_id, table_name)
                return redirect("/ranking")

            elif data[0]["action"] == 0:
                db.execute("UPDATE vote_check SET action = 1 WHERE id_owner = ? AND table_name = ? AND voter_id = ?", owner_id, table_name, session["user_id"])
                data_vote_table = db.execute("SELECT * FROM vote_table WHERE id_owner = ? AND table_name = ?", owner_id, table_name)
                sum_upvote = data_vote_table[0]["upvote"] + action
                db.execute("UPDATE vote_table SET upvote = ? WHERE id_owner = ? AND table_name = ?", sum_upvote, owner_id, table_name)                
                return redirect("/ranking")

            else:
                db.execute("UPDATE vote_check SET action = 2 WHERE id_owner = ? AND table_name = ? AND voter_id = ?", owner_id, table_name, session["user_id"])
                data_vote_table = db.execute("SELECT * FROM vote_table WHERE id_owner = ? AND table_name = ?", owner_id, table_name)
                sum_upvote = data_vote_table[0]["upvote"] + action
                db.execute("UPDATE vote_table SET upvote = ? WHERE id_owner = ? AND table_name = ?", sum_upvote, owner_id, table_name)
                return redirect("/ranking")

        else:
            data = db.execute("SELECT * FROM vote_check WHERE id_owner = ? AND table_name = ? AND voter_id = ?", owner_id, table_name, session["user_id"])
            if data[0]["action"] == -1 or data[0]["action"] == 2:
                if data[0]["action"] == -1:
                    db.execute("UPDATE vote_check SET action = 0 WHERE id_owner = ? AND table_name = ? AND voter_id = ?", owner_id, table_name, session["user_id"])
                else:
                    db.execute("UPDATE vote_check SET action = 1 WHERE id_owner = ? AND table_name = ? AND voter_id = ?", owner_id, table_name, session["user_id"])

                data_vote_table = db.execute("SELECT * FROM vote_table WHERE id_owner = ? AND table_name = ?", owner_id, table_name)
                sum_downvote = data_vote_table[0]["downvote"] + action
                db.execute("UPDATE vote_table SET downvote = ? WHERE id_owner = ? AND table_name = ?", sum_downvote, owner_id, table_name)                
                return redirect("/ranking")

            elif data[0]["action"] == 0:
                action = -action
                db.execute("UPDATE vote_check SET action = -1 WHERE id_owner = ? AND table_name = ? AND voter_id = ?", owner_id, table_name, session["user_id"])
                data_vote_table = db.execute("SELECT * FROM vote_table WHERE id_owner = ? AND table_name = ?", owner_id, table_name)
                sum_downvote = data_vote_table[0]["downvote"] + action
                db.execute("UPDATE vote_table SET downvote = ? WHERE id_owner = ? AND table_name = ?", sum_downvote, owner_id, table_name)                
                return redirect("/ranking")


            else:
                action = -action
                db.execute("UPDATE vote_check SET action = 2 WHERE id_owner = ? AND table_name = ? AND voter_id = ?", owner_id, table_name, session["user_id"])
                data_vote_table = db.execute("SELECT * FROM vote_table WHERE id_owner = ? AND table_name = ?", owner_id, table_name)
                sum_downvote = data_vote_table[0]["downvote"] + action
                db.execute("UPDATE vote_table SET downvote = ? WHERE id_owner = ? AND table_name = ?", sum_downvote, owner_id, table_name)
                return redirect("/ranking")
        