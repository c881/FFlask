from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///sample.db")

valid_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']
ERRORS = {"sum": "חסר סכום", "category": "לא בחרת קטגוריה", "categories": "קטגוריה לא קיימת",
          "values": "שדה סכום מכיל תוים מעבר לספרות ו/או/ נקודה"}


@app.route('/')
def index():
    """If the user isn't logged in, got to Login page.
        Else, if logged in - got to index and use the user name for personalize."""
    if not session.get("name"):
        return redirect("/login",)
    return render_template("index.html", user_name=session.get("name"),
                           categories=db.execute('SELECT * FROM categories ORDER BY category_id'),
                           pays=db.execute('SELECT * FROM payTypes ORDER BY TypeID'))


@app.route('/login', methods=["GET", "POST"])
def login():
    """the page work with both methods."""
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
    """We will add the expense to the sql table and return to enter a new expense.
        test the values for correctness."""
    sum_input = request.form.get("sum")
    if not sum_input:
        return render_template("error.html", message=ERRORS["sum"])
    for char in sum_input:
        if char not in valid_chars:
            return render_template("error.html", message=ERRORS["values"])

    category = int(request.form.get("categories"))
    if not category:
        return render_template("error.html", message=ERRORS["category"])

    rows = db.execute('SELECT category_id FROM categories where category_id  = (?)', int(category))
    if len(rows) == 0:
        return render_template("error.html", message=ERRORS["categories"])

    db.execute('INSERT INTO expenses VALUES (?, ?)', int(category), float(sum_input))
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
