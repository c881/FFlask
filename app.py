from flask import Flask, render_template, request, jsonify
app = Flask(__name__)


@app.route('/')
def index():
    # return "<h1>Welcome to our server !!</h1>" 1st step
    # return render_template("index.html") 2nd step
    # return render_template("index.html", name=request.args.get("name"))
    return render_template("index.html")


@app.route('/greet')
def greet():
    return render_template("greet.html", first_name=request.args.get("first_name","world"))


if __name__ == '__main__':
    app.run(threaded=True, port=5000)