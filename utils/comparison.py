import pandas as pd


def comparison_table(results):

    rows = []

    for result in results:

        rows.append({

            "Algorithm": result["algorithm"],

            "Root": round(result["root"], 8),

            "Iterations": result["iteration_count"],

            "Final Error": "{:.2e}".format(
                result["final_error"]
            ),

            "Converged": result["converged"]

        })

    return pd.DataFrame(rows)