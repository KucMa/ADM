from flask import Flask, render_template, request

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


class Serie:
    def __init__(self, module, multiplier, increment, seed):
        self.module = module
        self.multiplier = multiplier
        self.increment = increment
        self.seed = seed
        self.numbers = self.numbers_generator()

    def numbers_generator(self):
        numbers = [self.seed]
        x = self.seed
        x = (self.multiplier * x + self.increment) % self.module
        
        while x != self.seed:
            numbers.append(x)
            x = (self.multiplier * x + self.increment) % self.module

        return numbers