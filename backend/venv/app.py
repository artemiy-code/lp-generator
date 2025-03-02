import random
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

def generate_transportation_problem():
    warehouses = random.randint(3, 5)
    stores = random.randint(3, 5)

    # Генерируем случайные запасы и спрос
    supply = [random.randint(20, 50) for _ in range(warehouses)]
    demand = [random.randint(20, 50) for _ in range(stores)]

    # Приводим задачу к закрытому типу
    total_supply = sum(supply)
    total_demand = sum(demand)

    if total_supply > total_demand:
        demand[-1] += (total_supply - total_demand)
    elif total_demand > total_supply:
        supply[-1] += (total_demand - total_supply)

    # Генерируем таблицу стоимости перевозок
    cost_matrix = [[random.randint(1, 20) for _ in range(stores)] for _ in range(warehouses)]

    problem_text = (
        f"Дана транспортная задача с {warehouses} складами и {stores} магазинами. "
        f"Суммарный запас равен суммарному спросу ({sum(supply)}). "
        f"Необходимо определить оптимальный план перевозок с минимальными затратами."
    )

    # Формируем таблицу в HTML
    table = "<table><tr><th>Склады →</th>" + "".join(f"<th>Магазин {i+1}</th>" for i in range(stores)) + "<th>Запасы</th></tr>"
    for i in range(warehouses):
        table += f"<tr><th>Склад {i+1}</th>" + "".join(f"<td>{cost_matrix[i][j]}</td>" for j in range(stores)) + f"<td>{supply[i]}</td></tr>"
    table += "<tr><th>Потребности ↓</th>" + "".join(f"<td>{demand[j]}</td>" for j in range(stores)) + "<td></td></tr></table>"

    # Решаем методом северо-западного угла и считаем стоимость
    steps, total_cost = northwest_corner_method(supply[:], demand[:], cost_matrix)

    return {
        "description": problem_text,
        "details": table,
        "solution_steps": steps + f"<br><strong>Общая стоимость перевозок: {total_cost}</strong>"
    }

def northwest_corner_method(supply, demand, cost_matrix):
    steps = ["Опорный план: Метод северо-западного угла\n"]
    allocation = [[0] * len(demand) for _ in range(len(supply))]
    total_cost = 0  # Общая стоимость перевозок
    i, j = 0, 0

    while i < len(supply) and j < len(demand):
        allocation[i][j] = min(supply[i], demand[j])
        cost = allocation[i][j] * cost_matrix[i][j]
        total_cost += cost

        steps.append(f"Заполняем ячейку ({i+1}, {j+1}) значением {allocation[i][j]} (Стоимость: {cost})")

        supply[i] -= allocation[i][j]
        demand[j] -= allocation[i][j]

        if supply[i] == 0:
            i += 1
        if demand[j] == 0:
            j += 1

    return "<br>".join(steps), total_cost


def optimize_transportation_plan(allocation, cost_matrix):
    steps = []
    u = [None] * len(allocation)
    v = [None] * len(allocation[0])
    u[0] = 0  
    assigned = [(0, j) for j in range(len(v)) if allocation[0][j] > 0] + [(i, 0) for i in range(len(u)) if allocation[i][0] > 0]

    while assigned:
        i, j = assigned.pop(0)
        if u[i] is not None and v[j] is None:
            v[j] = cost_matrix[i][j] - u[i]
        elif v[j] is not None and u[i] is None:
            u[i] = cost_matrix[i][j] - v[j]
        assigned.extend([(x, j) for x in range(len(u)) if allocation[x][j] > 0 and u[x] is None])
        assigned.extend([(i, y) for y in range(len(v)) if allocation[i][y] > 0 and v[y] is None])

    delta = [[(u[i] + v[j] - cost_matrix[i][j]) if allocation[i][j] == 0 else None for j in range(len(v))] for i in range(len(u))]
    max_delta = max(((delta[i][j], i, j) for i in range(len(u)) for j in range(len(v)) if delta[i][j] is not None), default=(None, -1, -1))
    
    if max_delta[0] is None or max_delta[0] <= 0:
        steps.append("Оптимальное решение найдено.")
    else:
        steps.append(f"Оптимизация возможна, наибольшая положительная оценка: {max_delta[0]} в ячейке ({max_delta[1]+1}, {max_delta[2]+1})")
    
    total_cost = sum(allocation[i][j] * cost_matrix[i][j] for i in range(len(u)) for j in range(len(v)))
    return allocation, steps, total_cost

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
