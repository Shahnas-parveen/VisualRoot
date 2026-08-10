import matplotlib.pyplot as plt


def plot_convergence(results):

    fig, ax = plt.subplots(figsize=(8, 5))

    for result in results:

        errors = [
            step["error"]
            for step in result["iterations"]
        ]

        ax.semilogy(
            range(1, len(errors) + 1),
            errors,
            marker="o",
            label=result["algorithm"]
        )

    ax.set_xlabel("Iteration")

    ax.set_ylabel("Absolute Error")

    ax.set_title("Convergence Comparison")

    ax.grid(True)

    ax.legend()

    return fig