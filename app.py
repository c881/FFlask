from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
# import sqlite3


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///sample.db")

ERRORS = {"sum": "חסר סכום", "category": "לא בחרת קטגוריה", "categories": "קטגוריה לא קיימת"}


@app.route('/')
def index():
    if not session.get("name"):
        return redirect("/login",)
    return render_template("index.html", user_name=session.get("name"), categories=db.execute('SELECT * FROM categories ORDER BY category_id'))


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        session["name"] = request.form.get("name")
        return redirect("/")
    return render_template("login.html")


@app.route('/logout')
def logout():
    session["name"] = None
    return render_template("logout.html")


@app.route('/added', methods=["POST"])
def added():
    sum_input = request.form.get("sum")
    if not sum_input:
        return render_template("error.html", message=ERRORS["sum"])

    category = int(request.form.get("categories"))
    if not category:
        return render_template("error.html", message=ERRORS["category"])

    rows = db.execute('SELECT category_id FROM categories where category_id  = (?)', int(category))
    if len(rows) == 0:
        return render_template("error.html", message=ERRORS["categories"])

    db.execute('INSERT INTO expenses VALUES (?, ?)', int(category), sum_input)
    return redirect("/")


@app.route('/listed')
def checked():
    rows = db.execute('''SELECT a.category, a.sum, b.category_h_name 
                        FROM expenses a, 
                             categories b
                             where a.category = b.category_id ORDER BY category_id''')
    return render_template("listed.html", rows=rows)


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
