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
          "values": "שדה סכום מכיל תוים מעבר לספרות ו/או/ נקודה", "date": "תאריך חסר/ לא תקין",
          "pay": "סחר סוג תשלום/ תשלום שגוי", "num_of_pays": "חסר מספר תשלומים/ תשלומים = 0"}


@app.route('/')
@app.route('/en')
def index():
    """If the user isn't logged in, got to Login page.
        Else, if logged in - got to index and use the user name for personalize.
        Default page in english."""
    if not session.get("name"):
        return redirect("/login",)
    if not session.get("lang") or session.get("lang") == "en":
        return render_template("index.html", user_name=session.get("name"),
                           categories=db.execute('SELECT * FROM categories ORDER BY category_id'),
                           pays=db.execute('SELECT * FROM payTypes ORDER BY PayID'))
    else:
        return render_template("index_he.html", user_name=session.get("name"),
                               categories=db.execute('SELECT * FROM categories ORDER BY category_id'),
                               pays=db.execute('SELECT * FROM payTypes ORDER BY PayID'))

# @app.route('/he')
# def index_he():
#     """If the user isn't logged in, got to Login page.
#             Else, if logged in - got to index and use the user name for personalize.
#             For Hebrew users"""
#     if not session.get("name"):
#         return redirect("/login", )
#     return render_template("index_he.html", user_name=session.get("name"),
#                            categories=db.execute('SELECT * FROM categories ORDER BY category_id'),
#                            pays=db.execute('SELECT * FROM payTypes ORDER BY PayID'))


@app.route('/login', methods=["GET", "POST"])
def login():
    """the page work with both methods."""
    if request.method == 'POST':
        session["name"] = request.form.get("name")
        session["lang"] = request.form.get("lang")
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

    category_id = int(request.form.get("categories"))
    if not category_id:
        return render_template("error.html", message=ERRORS["category"])

    rows = db.execute('SELECT category_id FROM categories where category_id  = (?)', category_id)
    if len(rows) == 0:
        return render_template("error.html", message=ERRORS["categories"])

    pay_date = request.form.get("paydate")
    if not pay_date:
        return render_template("error.html", message=ERRORS["date"])

    pay_type_id = int(request.form.get("pays"))
    if not pay_type_id:
        return render_template("error.html", message=ERRORS["pay"])

    rows = db.execute('SELECT PayId FROM payTypes where PayId  = (?)', pay_type_id)
    if len(rows) == 0:
        return render_template("error.html", message=ERRORS["pay"])

    num_of_pays = request.form.get("settlements")
    if not num_of_pays:
        return render_template("error.html", message=ERRORS["num_of_pays"])
    num_of_pays = int(num_of_pays)
    if num_of_pays == 0:
        return render_template("error.html", message=ERRORS["num_of_pays"])

    db.execute('INSERT INTO expenses VALUES (?, ?, ?, ?, ?)', category_id, float(sum_input), pay_type_id, num_of_pays,
               pay_date)
    return redirect("/")


@app.route('/listed')
def checked():
    rows = db.execute('''SELECT a.categoryID, 
                                a.sum, 
                                b.category_h_name,
                                c.PayName,
                                a.NumOfPays,
                                a.DateOfPay 
                        FROM expenses a, 
                             categories b,
                             paytypes c
                             where a.categoryID = b.category_id
                               and a.PayTypeId = c.PayID 
                             ORDER BY category_id, DateOfPay''')
    return render_template("listed.html", rows=rows)


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
