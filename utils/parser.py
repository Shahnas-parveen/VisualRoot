# This module handles parsing mathematical equations entered by the user.

import sympy as sp


def parse_equation(equation: str):
    x = sp.symbols("x")
    expression = sp.sympify(equation)
    return x, expression


def get_function(equation: str):
    x, expression = parse_equation(equation)

    f = sp.lambdify(x, expression, "numpy")

    return f


def get_functions(equation: str):
    x, expression = parse_equation(equation)

    derivative = sp.diff(expression, x)

    f = sp.lambdify(x, expression, "numpy")
    df = sp.lambdify(x, derivative, "numpy")

    return f, df