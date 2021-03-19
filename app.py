from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

ERRORS = {"sum": "חסר סכום", "category": "לא בחרת קטגוריה", "categories": "קטגוריה לא קיימת"}
EXPENSES = {}
CATEGORIES = {"fuel": " דלק", "food": " אוכל", "education": " חינוך", "clothes": "בגדים", "Health": "בריאות",
              "holidays": "חגים", "insurance": "ביטוח", "mortgage": "משכנתה", "taxes": "מיסים"}


@app.route('/')
def index():
    return render_template("index.html", categories=CATEGORIES)


@app.route('/added', methods=["POST"])
def added():
    # if not request.form.get("sum") or request.form.get("categories") not in CATEGORIES:
    #    return render_template("failure.html")
    # return render_template("success.html")
    sum_input = request.form.get("sum")
    if not sum_input:
        return render_template("error.html", message=ERRORS["sum"])

    category = request.form.get("categories")
    if not category:
        return render_template("error.html", message=ERRORS["category"])

    if category not in CATEGORIES:
        return render_template("error.html", message=ERRORS["categories"])


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
