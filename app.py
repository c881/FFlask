from cs50 import SQL
from flask import Flask, redirect, render_template, request, jsonify
# import sqlite3


app = Flask(__name__)

db = SQL("sqlite:///sample.db")

# EXPENSES = []
ERRORS = {"sum": "חסר סכום", "category": "לא בחרת קטגוריה", "categories": "קטגוריה לא קיימת"}
CATEGORIES = {"fuel": " דלק", "food": " אוכל", "education": " חינוך", "clothes": "בגדים", "Health": "בריאות",
              "holidays": "חגים", "insurance": "ביטוח", "mortgage": "משכנתה", "taxes": "מיסים"}


@app.route('/')
def index():
    return render_template("index.html", categories=CATEGORIES)


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

    # EXPENSES.append((category, sum_input))

    # con = sqlite3.connect('sample.db')
    # cur = con.cursor()
    # cur.execute('INSERT INTO expenses VALUES (?, ?)', (category, sum_input))
    # con.commit()
    db.execute('INSERT INTO expenses VALUES (?, ?)', category, sum_input)
    return redirect("/")


@app.route('/listed')
def checked():
    # con = sqlite3.connect('sample.db')
    # cur = con.cursor()
    # cur.execute('SELECT * FROM expenses ORDER BY category')
    # rows = cur.fetchall()
    rows = db.execute('SELECT * FROM expenses ORDER BY category')
    return render_template("listed.html", rows=rows, categories=CATEGORIES)


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
