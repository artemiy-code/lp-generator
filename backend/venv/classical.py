import random
import numpy as np

def generate_classic_lp_problem():
    num_vars = random.randint(2, 3)
    num_constraints = random.randint(2, 3)

    coefficients = [random.randint(1, 10) for _ in range(num_vars)]
    constraints = [[random.randint(1, 10) for _ in range(num_vars)] for _ in range(num_constraints)]
    rhs = [random.randint(10, 50) for _ in range(num_constraints)]

    objective_type = random.choice(["максимизировать", "минимизировать", "максимизировать"])
    problem_text = (
        f"Дана классическая задача линейного программирования. "
        f"Требуется {objective_type} функцию:"
    )

    objective_function = "F = " + " + ".join(f"{coefficients[i]}x{i+1}" for i in range(num_vars))

    constraint_text = "<br>".join(
        " + ".join(f"{constraints[j][i]}x{i+1}" for i in range(num_vars)) + f" ≤ {rhs[j]}"
        for j in range(num_constraints)
    )

    details = f"<p>{objective_function} → { 'максимум' if objective_type == 'максимизировать' else 'минимум' }</p><p>Ограничения:</p><p>{constraint_text}</p>"

    steps = simplex_method_with_steps(coefficients, constraints, rhs, objective_type)

    return {
        "description": problem_text,
        "details": details,
        "solution_steps": steps
    }


def simplex_method_with_steps(c, A, b, objective_type):
    steps = []
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    c = np.array(c, dtype=float)

    if objective_type == "максимизировать":
        c = -c

    num_constraints, num_vars = A.shape

    tableau = np.hstack((A, np.eye(num_constraints), b.reshape(-1, 1)))
    c_row = np.hstack((c, np.zeros(num_constraints + 1)))
    tableau = np.vstack((tableau, c_row))

    steps.append("Симплекс-таблица с дельтами")
    steps.append(format_tableau(tableau))

    iteration = 1
    while np.min(tableau[-1, :-1]) < 0:
        steps.append(f"<br><strong>Итерация {iteration}</strong>")
        pivot_col = np.argmin(tableau[-1, :-1])
        if all(tableau[:-1, pivot_col] <= 0):
            steps.append("Решение не ограничено.")
            return "<br>".join(steps)

        ratios = []
        for i in range(num_constraints):
            if tableau[i, pivot_col] > 0:
                ratios.append(tableau[i, -1] / tableau[i, pivot_col])
            else:
                ratios.append(np.inf)

        pivot_row = np.argmin(ratios)
        pivot_element = tableau[pivot_row, pivot_col]

        tableau[pivot_row] /= pivot_element
        for i in range(len(tableau)):
            if i != pivot_row:
                tableau[i] -= tableau[i, pivot_col] * tableau[pivot_row]

        steps.append(f"Разрешающий элемент: ({pivot_row + 1}, {pivot_col + 1}) = {round(pivot_element, 2)}")
        steps.append("Симплекс-таблица с обновленными дельтами")
        steps.append(format_tableau(tableau))

        iteration += 1

    var_values = [0] * num_vars
    for i in range(num_constraints):
        pivot_col_indices = np.where(tableau[i, :num_vars] == 1)[0]
        if len(pivot_col_indices) == 1 and all(tableau[:, pivot_col_indices[0]][j] == (1 if j == i else 0) for j in range(num_constraints)):
            var_values[pivot_col_indices[0]] = tableau[i, -1]

    var_output = "<br>".join([f"x{i+1} = {round(val, 2)}" for i, val in enumerate(var_values)])
    z = round(tableau[-1, -1], 2)

    steps.append(f"<br><strong>Оптимальные значения переменных:</strong><br>{var_output}")
    steps.append(f"<br><strong>Значение целевой функции:</strong> F = {z}")
    return "<br>".join(steps)


def format_tableau(tableau):
    formatted = "<table border='1' style='margin: auto;'>"
    for row in tableau:
        formatted += "<tr>" + "".join(f"<td>{round(val, 2)}</td>" for val in row) + "</tr>"
    formatted += "</table>"
    return formatted