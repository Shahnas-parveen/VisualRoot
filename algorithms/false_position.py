from utils.parser import get_function
from utils.helpers import create_result


def false_position_method(params):

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

        fa = f(a)
        fb = f(b)

        c = (a * fb - b * fa) / (fb - fa)
        fc = f(c)

        error = abs(fc)

        iterations.append({
            "iteration": i + 1,
            "a": a,
            "b": b,
            "x": c,
            "fx": fc,
            "error": error
        })

        if abs(fc) < tolerance:
            return create_result(
                "False Position",
                c,
                iterations,
                True
            )

        if fa * fc < 0:
            b = c
        else:
            a = c

    return create_result(
        "False Position",
        c,
        iterations,
        False
    )