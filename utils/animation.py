import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


def animate_iterations(equation, iterations):

    x = sp.symbols("x")
    expr = sp.sympify(equation)
    f = sp.lambdify(x, expr, "numpy")

    xs = np.linspace(-5, 5, 500)
    ys = f(xs)

    for step in iterations:

        fig, ax = plt.subplots(figsize=(8, 5))

        ax.plot(xs, ys, color="royalblue")

        ax.axhline(0, color="black")

        current = step["x"]

        ax.scatter(
            current,
            f(current),
            s=120,
            color="red",
            zorder=5
        )

        ax.set_title(
            f"Iteration {step['iteration']}"
        )

        ax.grid(True)

        yield fig