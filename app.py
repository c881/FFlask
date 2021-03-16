from flask import Flask, render_template, request, jsonify
app = Flask(__name__)


@app.route('/')
def index():

    return render_template("index.html")

@app.route('/added', methods=["POST"])
def added():
    if not request.form.get("sum") or not request.form.get("categories"):
        return render_template("failure.html")
    return render_template("success.html")


if __name__ == '__main__':
    app.run(threaded=True, port=5000)