from flask import Flask, render_template, jsonify, request
from classical import generate_classic_lp_problem
from transportation import generate_transportation_problem


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate")
def generate():
    problem_type = request.args.get("type", "transportation")
    if problem_type == "transportation":
        problem = generate_transportation_problem()
    else:
        problem = generate_classic_lp_problem()
    return jsonify(problem)

if __name__ == "__main__":
    print("Сервер запущен: http://127.0.0.1:5000")
    app.run(debug=True, host="127.0.0.1", port=5000)
