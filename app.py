from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
# import sqlite3


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///sample.db")

# EXPENSES = []
ERRORS = {"sum": "חסר סכום", "category": "לא בחרת קטגוריה", "categories": "קטגוריה לא קיימת"}
CATEGORIES = {"fuel": " דלק", "food": " אוכל", "education": " חינוך", "clothes": "בגדים", "Health": "בריאות",
              "holidays": "חגים", "insurance": "ביטוח", "mortgage": "משכנתה", "taxes": "מיסים"}


@app.route('/')
def index():
    if not session.get("name"):
        return redirect("/login",)
    return render_template("index.html", categories=CATEGORIES)


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

    category = request.form.get("categories")
    if not category:
        return render_template("error.html", message=ERRORS["category"])

    if category not in CATEGORIES:
        return render_template("error.html", message=ERRORS["categories"])

    db.execute('INSERT INTO expenses VALUES (?, ?)', category, sum_input)
    return redirect("/")


@app.route('/listed')
def checked():
    rows = db.execute('SELECT * FROM expenses ORDER BY category')
    return render_template("listed.html", rows=rows, categories=CATEGORIES)


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
