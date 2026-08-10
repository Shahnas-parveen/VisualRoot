from utils.parser import get_function
from utils.helpers import create_result


def fixed_point_method(params):

    equation = params["equation"]
    x0 = params["x0"]
    tolerance = params["tolerance"]
    max_iterations = params["max_iterations"]
    g = get_function(equation)

    iterations = []

    for i in range(max_iterations):

        x1 = g(x0)

        error = abs(x1 - x0)

        iterations.append({
            "iteration": i + 1,
            "x": x1,
            "fx": x1,
            "error": error
        })

        if error < tolerance:
            return create_result(
                "Fixed Point",
                x1,
                iterations,
                True
            )

        x0 = x1

    return create_result(
        "Fixed Point",
        x1,
        iterations,
        False
    )