from cs50 import SQL
from flask import Flask, jsonify, redirect, render_template, request, session
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
def index():
    """If the user isn't logged in, got to Login page.
        Else, if logged in - got to index and use the user name for personalize.
        Default page in english."""

    if not session.get("name"):
        return redirect("/login",)

    categories = db.execute('SELECT * FROM categories ORDER BY category_id')
    pays = db.execute('SELECT * FROM payTypes ORDER BY pay_id')
    user_name = session.get("name")
    if not session.get("lang") or session.get("lang") == "en":
        user_lang = "en"
        headlines = db.execute('''SELECT title_id, title_e_name as name
                               FROM headlines 
                               WHERE screen_id="index"''')
    else:
        user_lang = "he"
        headlines = db.execute('''SELECT title_id, title_h_name as name 
                                       FROM headlines 
                                       WHERE screen_id="index"''')
    dict_headlines = {}
    for headline in headlines:
        dict_headlines[headline['title_id']] = headline['name']
    # headlines = jsonify(headlines)
    return render_template("index.html", user_name=user_name, user_lang=user_lang,
                           categories=categories, pays=pays, headlines=dict_headlines)



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
    sum_input = float(sum_input)
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

    rows = db.execute('SELECT Pay_Id FROM payTypes where Pay_Id  = (?)', pay_type_id)
    if len(rows) == 0:
        return render_template("error.html", message=ERRORS["pay"])

    num_of_pays = request.form.get("settlements")
    if not num_of_pays:
        return render_template("error.html", message=ERRORS["num_of_pays"])
    num_of_pays = int(num_of_pays)
    if num_of_pays == 0:
        return render_template("error.html", message=ERRORS["num_of_pays"])

    db.execute('INSERT INTO expenses VALUES (?, ?, ?, ?, ?)', category_id, sum_input, pay_type_id,
               num_of_pays, pay_date)
    return redirect("/")


@app.route('/listed')
def checked():
    user_lang = session.get("lang")
    rows = db.execute('''SELECT a.category_id, 
                                a.sum, 
                                b.category_h_name,
                                c.pay_h_name,
                                c.pay_e_name,
                                a.Num_Of_Pays,
                                a.Date_Of_Pay 
                        FROM expenses a, 
                             categories b,
                             paytypes c
                             where a.category_id = b.category_id
                               and a.Pay_Type_Id = c.Pay_ID 
                             ORDER BY a.category_id, Date_Of_Pay''')
    return render_template("listed.html", rows=rows, user_lang=user_lang)


@app.route('/summed')
def checked():
    user_lang = session.get("lang")
    rows = db.execute('''SELECT a.category_id, 
                                sum(a.sum) as summed, 
                                b.category_h_name,
                                c.pay_h_name,
                                c.pay_e_name,
                                a.Num_Of_Pays,
                                a.Date_Of_Pay 
                        FROM expenses a, 
                             categories b,
                             paytypes c
                             where a.category_id = b.category_id
                               and a.Pay_Type_Id = c.Pay_ID
                             group by a.category_id
                             ORDER BY a.category_id, Date_Of_Pay''')
    return render_template("listed.html", rows=rows, user_lang=user_lang)


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
