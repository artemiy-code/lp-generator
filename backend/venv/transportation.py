import random

def generate_transportation_problem():
    warehouses = random.randint(3, 5)
    stores = random.randint(3, 5)
    if (warehouses + stores == 6):
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
    table = "<table><tr><th>Склады ↓</th>" + "".join(f"<th>Магазин {i+1}</th>" for i in range(stores)) + "<th>Запасы</th></tr>"
    for i in range(warehouses):
        table += f"<tr><th>Склад {i+1}</th>" + "".join(f"<td>{cost_matrix[i][j]}</td>" for j in range(stores)) + f"<td>{supply[i]}</td></tr>"
    table += "<tr><th>Потребности →</th>" + "".join(f"<td>{demand[j]}</td>" for j in range(stores)) + "<td></td></tr></table>"

    # Решаем методом северо-западного угла и считаем стоимость
    steps, total_cost, allocation = northwest_corner_method(supply[:], demand[:], cost_matrix)
    optimization_steps = optimize_plan(allocation, cost_matrix)

    return {
        "description": problem_text,
        "details": table,
        "solution_steps": steps + f"<br><strong>Общая стоимость перевозок: {total_cost}</strong>" + optimization_steps
    }


def northwest_corner_method(supply, demand, cost_matrix):
    steps = ["<strong>Опорный план: Метод северо-западного угла</strong><br>"]
    allocation = [[0] * len(demand) for _ in range(len(supply))]
    total_cost = 0
    i, j = 0, 0

    while i < len(supply) and j < len(demand):
        alloc = min(supply[i], demand[j])
        allocation[i][j] = alloc
        cost = alloc * cost_matrix[i][j]
        total_cost += cost

        steps.append(f"Заполняем ячейку ({i+1}, {j+1}) значением {alloc} (Стоимость: {cost})")

        supply[i] -= alloc
        demand[j] -= alloc

        if supply[i] == 0 and i < len(supply) - 1:
            i += 1
        elif demand[j] == 0 and j < len(demand) - 1:
            j += 1
        else:
            break

    # Генерация HTML-таблицы с распределениями
    table_html = "<br><br><strong>Таблица распределений:</strong><br><table border='1' cellpadding='5'><tr><th></th>"
    for j in range(len(demand)):
        table_html += f"<th>Магазин {j+1}</th>"
    table_html += "</tr>"

    for i in range(len(supply)):
        table_html += f"<tr><th>Склад {i+1}</th>"
        for j in range(len(demand)):
            val = allocation[i][j]
            if val > 0:
                table_html += f"<td><strong>{val}</strong><br><small>({cost_matrix[i][j]})</small></td>"
            else:
                table_html += f"<td><small>{cost_matrix[i][j]}</small></td>"
        table_html += "</tr>"
    table_html += "</table>"

    return "<br>".join(steps) + table_html, total_cost, allocation


def optimize_plan(allocation, cost_matrix):
    rows, cols = len(allocation), len(allocation[0])
    steps = ["<br><strong>Оптимизация методом потенциалов:</strong><br>"]

    while True:
        u = [None] * rows
        v = [None] * cols
        u[0] = 0
        basis = [(i, j) for i in range(rows) for j in range(cols) if allocation[i][j] > 0]

        updated = True
        while updated:
            updated = False
            for i, j in basis:
                if u[i] is not None and v[j] is None:
                    v[j] = cost_matrix[i][j] - u[i]
                    updated = True
                elif v[j] is not None and u[i] is None:
                    u[i] = cost_matrix[i][j] - v[j]
                    updated = True

        deltas = [[None for _ in range(cols)] for _ in range(rows)]
        min_delta = 0
        entering = None
        for i in range(rows):
            for j in range(cols):
                if allocation[i][j] == 0 and u[i] is not None and v[j] is not None:
                    delta = cost_matrix[i][j] - u[i] - v[j]
                    deltas[i][j] = delta
                    if delta < min_delta:
                        min_delta = delta
                        entering = (i, j)

        if entering is None:
            steps.append("Все оценки неотрицательные — найден оптимальный план.")
            break

        steps.append(f"Найдена отрицательная оценка Δ({entering[0]+1},{entering[1]+1}) = {min_delta}. Перестраиваем план...")

        cycle = find_cycle(allocation, entering)
        if not cycle:
            steps.append("Цикл не найден — ошибка в построении.")
            break

        even_cells = cycle[1::2]
        min_val = min(allocation[i][j] for i, j in even_cells)

        for k, (i, j) in enumerate(cycle):
            if k % 2 == 0:
                allocation[i][j] += min_val
            else:
                allocation[i][j] -= min_val
                if allocation[i][j] == 0:
                    basis.remove((i, j))

        basis.append(entering)

    total_cost = sum(allocation[i][j] * cost_matrix[i][j] for i in range(rows) for j in range(cols))
    steps.append(f"<br><strong>Итоговая стоимость: {total_cost}</strong>")
    return "<br>".join(steps)

def find_cycle(allocation, start):
    from collections import defaultdict

    rows, cols = len(allocation), len(allocation[0])
    basic_cells = [(i, j) for i in range(rows) for j in range(cols) if allocation[i][j] > 0 or (i, j) == start]

    # Создаем словари для быстрого доступа по строкам и столбцам
    row_dict = defaultdict(list)
    col_dict = defaultdict(list)
    for i, j in basic_cells:
        row_dict[i].append((i, j))
        col_dict[j].append((i, j))

    def dfs(path, visited, horizontal):
        last = path[-1]
        neighbors = row_dict[last[0]] if horizontal else col_dict[last[1]]

        for nei in neighbors:
            if nei == start and len(path) >= 4:
                return path + [start]
            if nei in visited or nei == last:
                continue
            result = dfs(path + [nei], visited | {nei}, not horizontal)
            if result:
                return result
        return None

    return dfs([start], {start}, True)
