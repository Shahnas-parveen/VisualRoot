from utils.parser import get_function
from utils.helpers import create_result


def bisection_method(params):

    equation = params["equation"]
    a = params["a"]
    b = params["b"]
    tolerance = params["tolerance"]
    max_iterations = params["max_iterations"]
    f = get_function(equation)

    if f(a) * f(b) > 0:
        raise ValueError("Invalid interval. f(a) and f(b) must have opposite signs.")

    iterations = []

    for i in range(max_iterations):

        c = (a + b) / 2
        fc = f(c)

        error = abs(b - a) / 2

        iterations.append({
            "iteration": i + 1,
            "a": a,
            "b": b,
            "x": c,
            "fx": fc,
            "error": error
        })

        if abs(fc) < tolerance or error < tolerance:
            return create_result(
                "Bisection",
                c,
                iterations,
                True
            )

        if f(a) * fc < 0:
            b = c
        else:
            a = c

    return create_result(
        "Bisection",
        c,
        iterations,
        False
    )