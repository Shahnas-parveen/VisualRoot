import numpy as np
import matplotlib.pyplot as plt

from utils.parser import get_function


def plot_iterations(equation, iterations, root):

    f = get_function(equation)

    x_values = [step["x"] for step in iterations]

    xmin = min(x_values) - 1
    xmax = max(x_values) + 1

    x = np.linspace(xmin, xmax, 500)
    y = f(x)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(x, y, label="f(x)", linewidth=2)

    ax.axhline(0, color="black", linewidth=0.8)

    for step in iterations:

        xi = step["x"]
        yi = f(xi)

        ax.scatter(xi, yi, s=60)

        ax.text(
            xi,
            yi,
            f"x{step['iteration']}",
            fontsize=9
        )

    ax.scatter(
        root,
        f(root),
        marker="*",
        s=180,
        label="Root"
    )

    ax.set_title("Root Finding Visualization")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")

    ax.grid(True)

    ax.legend()

    return fig