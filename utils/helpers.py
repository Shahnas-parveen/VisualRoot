def create_result(algorithm, root, iterations, converged):

    return {
        "algorithm": algorithm,
        "root": root,
        "iterations": iterations,
        "iteration_count": len(iterations),
        "final_error": iterations[-1]["error"] if iterations else None,
        "converged": converged
    }