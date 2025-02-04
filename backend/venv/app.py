import random
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

def generate_transportation_problem():
    warehouses = random.randint(2, 4)
    stores = random.randint(2, 4)

    supply = [random.randint(20, 50) for _ in range(warehouses)]
    demand = [random.randint(20, 50) for _ in range(stores)]

    cost_matrix = [[random.randint(1, 20) for _ in range(stores)] for _ in range(warehouses)]

    problem_text = (
        f"Дана транспортная задача с {warehouses} складами и {stores} магазинами. "
        f"Необходимо определить оптимальный план перевозок с минимальными затратами."
    )

    table = "<table><tr><th>Склады →</th>" + "".join(f"<th>Магазин {i+1}</th>" for i in range(stores)) + "<th>Запасы</th></tr>"
    for i in range(warehouses):
        table += f"<tr><th>Склад {i+1}</th>" + "".join(f"<td>{cost_matrix[i][j]}</td>" for j in range(stores)) + f"<td>{supply[i]}</td></tr>"
    table += "<tr><th>Потребности ↓</th>" + "".join(f"<td>{demand[j]}</td>" for j in range(stores)) + "<td></td></tr></table>"

    return {"description": problem_text, "details": table}

def generate_classic_lp_problem():
    num_vars = random.randint(2, 4)
    num_constraints = random.randint(2, 4)

    coefficients = [random.randint(1, 10) for _ in range(num_vars)]
    constraints = [[random.randint(1, 10) for _ in range(num_vars)] + [random.randint(10, 50)] for _ in range(num_constraints)]

    objective_type = random.choice(["максимизировать", "минимизировать"])

    problem_text = (
        f"Дана классическая задача линейного программирования. "
        f"Требуется {objective_type} функцию:\n"
    )

    objective_function = "F = " + " + ".join(f"{coefficients[i]}x{i+1}" for i in range(num_vars))

    constraint_text = "<br>".join(
        " + ".join(f"{constraints[j][i]}x{i+1}" for i in range(num_vars)) + f" ≤ {constraints[j][-1]}"
        for j in range(num_constraints)
    )

    details = f"<p>{objective_function} → {objective_type}</p><p>Ограничения:</p><p>{constraint_text}</p>"

    return {"description": problem_text, "details": details}

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
