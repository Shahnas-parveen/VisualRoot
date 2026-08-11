import numpy as np
import matplotlib.pyplot as plt

from utils.parser import get_function


def create_animation_frames(equation, iterations):

    f = get_function(equation)

    frames = []

    for i, step in enumerate(iterations):

        current_x = float(step["x"])

        # --------------------------------
        # Points up to current iteration
        # --------------------------------

        visible_steps = iterations[:i + 1]

        points_x = [
            float(s["x"])
            for s in visible_steps
        ]

        points_y = [
            float(f(s["x"]))
            for s in visible_steps
        ]

        # --------------------------------
        # Dynamic zoom
        # --------------------------------

        if "a" in step and "b" in step:

            a = float(step["a"])
            b = float(step["b"])

            interval_width = abs(b - a)

            if interval_width == 0:
                interval_width = 0.1

            margin = max(interval_width * 0.8, 0.05)

            xmin = min(a, current_x) - margin
            xmax = max(b, current_x) + margin

        else:

            if len(points_x) > 1:

                xmin = min(points_x)
                xmax = max(points_x)

                width = xmax - xmin

                if width == 0:
                    width = 0.1

                margin = max(width * 0.6, 0.1)

                xmin -= margin
                xmax += margin

            else:

                xmin = current_x - 1
                xmax = current_x + 1

        # --------------------------------
        # Function curve
        # --------------------------------

        x = np.linspace(xmin, xmax, 500)

        try:
            y = np.asarray(f(x), dtype=float)
        except Exception:
            y = np.array(
                [f(value) for value in x],
                dtype=float
            )

        # --------------------------------
        # Figure
        # --------------------------------

        fig, ax = plt.subplots(
            figsize=(10, 6)
        )

        ax.plot(
            x,
            y,
            linewidth=2.5,
            label="f(x)"
        )

        ax.axhline(
            0,
            color="black",
            linewidth=1
        )

        # --------------------------------
        # Previous points
        # --------------------------------

        if i > 0:

            ax.scatter(
                points_x[:-1],
                points_y[:-1],
                s=45,
                alpha=0.55,
                label="Previous iterations",
                zorder=3
            )

        # --------------------------------
        # Current point
        # --------------------------------

        current_y = float(f(current_x))

        ax.scatter(
            current_x,
            current_y,
            s=130,
            marker="o",
            zorder=6,
            label="Current"
        )

        # --------------------------------
        # Current point guide
        # --------------------------------

        ax.axvline(
            current_x,
            linestyle=":",
            linewidth=1,
            alpha=0.45
        )

        # --------------------------------
        # Bisection / False Position
        # --------------------------------

        if "a" in step and "b" in step:

            a = float(step["a"])
            b = float(step["b"])

            ax.axvspan(
                a,
                b,
                alpha=0.12,
                label="Search interval"
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

        # --------------------------------
        # Final root
        # --------------------------------

        if i == len(iterations) - 1:

            ax.scatter(
                current_x,
                current_y,
                marker="*",
                s=350,
                edgecolors="black",
                linewidths=2,
                zorder=10,
                label="Root"
            )

        # --------------------------------
        # Information panel
        # --------------------------------

        info = (
            f"Iteration: {step['iteration']}\n"
            f"xₙ = {current_x:.10f}\n"
            f"f(xₙ) = {current_y:.6e}"
        )

        if "a" in step and "b" in step:

            info += (
                f"\na = {float(step['a']):.10f}"
                f"\nb = {float(step['b']):.10f}"
            )

        ax.text(
            0.02,
            0.97,
            info,
            transform=ax.transAxes,
            verticalalignment="top",
            fontsize=11,
            fontweight="bold",
            bbox=dict(
                boxstyle="round,pad=0.5",
                alpha=0.85
            )
        )

        # --------------------------------
        # Formatting
        # --------------------------------

        ax.set_title(
            "Root Finding — Iteration Animation",
            fontsize=16,
            fontweight="bold"
        )

        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")

        ax.grid(
            True,
            alpha=0.25
        )

        ax.legend(
            loc="best"
        )

        fig.tight_layout()

        frames.append(fig)

    return frames