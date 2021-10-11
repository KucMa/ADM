from flask import Flask, render_template, request
from .models import Serie

app = Flask(__name__)
app.config.from_object("config")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/series_generator', methods=["POST", "GET"])
def series_generator():
    if request.method == "GET":
        return render_template("series_generator.html")
    else:
        serie = Serie(int(request.form["module"]), int(request.form["multiplier"]), int(request.form["increment"]), int(request.form["seed"]))

        return render_template("series_generator.html", serie = serie)