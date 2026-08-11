import numpy as np
import matplotlib.pyplot as plt

from utils.parser import get_function


def plot_iterations(equation, iterations, root):

    f = get_function(equation)

    x_values = np.array(
        [step["x"] for step in iterations],
        dtype=float
    )

    # -----------------------------
    # Dynamic X range
    # -----------------------------

    xmin = min(x_values) - 0.15
    xmax = max(x_values) + 0.15

    # Include interval endpoints if available
    for step in iterations:
        if "a" in step and "b" in step:
            xmin = min(xmin, step["a"])
            xmax = max(xmax, step["b"])

    x = np.linspace(xmin, xmax, 600)
    y = f(x)

    fig, ax = plt.subplots(figsize=(10, 6))

    # Function
    ax.plot(
        x,
        y,
        linewidth=2.5,
        label="f(x)"
    )

    # x-axis
    ax.axhline(
        0,
        color="black",
        linewidth=0.8
    )

    # -----------------------------
    # Previous iteration points
    # -----------------------------

    if len(iterations) > 1:

        previous_x = [
            step["x"]
            for step in iterations[:-1]
        ]

        previous_y = [
            f(step["x"])
            for step in iterations[:-1]
        ]

        ax.scatter(
            previous_x,
            previous_y,
            s=45,
            alpha=0.7,
            label="Iterations",
            zorder=3
        )

        # Labels
        for step in iterations[:-1]:

            xi = step["x"]
            yi = f(xi)

            ax.annotate(
                f"x{step['iteration']}",
                (xi, yi),
                xytext=(5, 5),
                textcoords="offset points",
                fontsize=8
            )

    # -----------------------------
    # Current iteration
    # -----------------------------

    current = iterations[-1]

    cx = current["x"]
    cy = f(cx)

    ax.scatter(
        cx,
        cy,
        s=100,
        marker="o",
        label="Current",
        zorder=5
    )

    # -----------------------------
    # Final root
    # -----------------------------

    ax.scatter(
        root,
        f(root),
        marker="*",
        s=300,
        edgecolors="black",
        linewidths=2,
        label="Root",
        zorder=6
    )

    # -----------------------------
    # Bisection / False Position
    # -----------------------------

    if "a" in current and "b" in current:

        a = current["a"]
        b = current["b"]

        ax.axvspan(
            a,
            b,
            alpha=0.12,
            label="Current interval"
        )

        ax.axvline(
            a,
            linestyle="--",
            linewidth=1,
            alpha=0.6
        )

        ax.axvline(
            b,
            linestyle="--",
            linewidth=1,
            alpha=0.6
        )

        # Endpoint labels
        ax.text(
            a,
            0,
            " a",
            fontsize=9,
            verticalalignment="bottom"
        )

        ax.text(
            b,
            0,
            " b",
            fontsize=9,
            verticalalignment="bottom"
        )

    # -----------------------------
    # Formatting
    # -----------------------------

    ax.set_title(
        "Root Finding Visualization",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")

    ax.grid(
        True,
        alpha=0.25
    )

    ax.legend()

    fig.tight_layout()

    return fig