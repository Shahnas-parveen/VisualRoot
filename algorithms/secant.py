from utils.parser import get_function
from utils.helpers import create_result


def secant_method(params):

    equation = params["equation"]
    x0 = params["x0"]
    x1 = params["x1"]
    tolerance = params["tolerance"]
    max_iterations = params["max_iterations"]
    f = get_function(equation)

    iterations = []

    for i in range(max_iterations):

        f0 = f(x0)
        f1 = f(x1)

        if abs(f1 - f0) < 1e-12:
            raise ValueError("Division by zero encountered.")

        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)

        error = abs(x2 - x1)

        iterations.append({
            "iteration": i + 1,
            "x0": x0,
            "x1": x1,
            "x": x2,
            "fx": f(x2),
            "error": error
        })

        if error < tolerance:
            return create_result(
                "Secant",
                x2,
                iterations,
                True
            )

        x0 = x1
        x1 = x2

    return create_result(
        "Secant",
        x2,
        iterations,
        False
    )