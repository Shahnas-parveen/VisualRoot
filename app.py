import streamlit as st
import time

from algorithms.registry import ALGORITHMS
from utils.plotting import plot_iterations
from utils.convergence import plot_convergence
from utils.comparison import comparison_table
from utils.animation import create_animation_frames


# =========================
# Page Configuration
# =========================

st.set_page_config(
    page_title="VisualRoot",
    page_icon="🧮",
    layout="wide"
)


# =========================
# Session State
# =========================

if "result" not in st.session_state:
    st.session_state.result = None

if "equation" not in st.session_state:
    st.session_state.equation = ""


# =========================
# Main Header
# =========================

st.title("🧮 VisualRoot")
st.caption("Interactive Numerical Root Finding Toolkit")
st.divider()


# =========================
# Sidebar
# =========================

st.sidebar.title("VisualRoot")

mode = st.sidebar.radio(
    "Mode",
    [
        "Single Algorithm",
        "Compare Algorithms"
    ]
)

st.sidebar.divider()


# ============================================================
# SINGLE ALGORITHM MODE
# ============================================================

if mode == "Single Algorithm":

    st.sidebar.subheader("Solver")

    algorithm = st.sidebar.selectbox(
        "Algorithm",
        list(ALGORITHMS.keys())
    )

    if algorithm == "Fixed Point":

        equation = st.sidebar.text_input(
            "Equation / g(x)",
            "(x + 1)**(1/3)"
        )

    else:

        equation = st.sidebar.text_input(
            "Equation",
            "x**3 - x - 1"
        )
    
    tolerance = st.sidebar.number_input(
        "Tolerance",
        value=1e-6,
        format="%.8f"
    )

    max_iterations = st.sidebar.number_input(
        "Maximum Iterations",
        min_value=1,
        value=100
    )

    params = {
        "equation": equation,
        "tolerance": tolerance,
        "max_iterations": max_iterations
    }


    # -------------------------
    # Algorithm Parameters
    # -------------------------

    if algorithm == "Newton-Raphson":

        params["x0"] = st.sidebar.number_input(
            "Initial Guess",
            value=1.5
        )

    elif algorithm in ["Bisection", "False Position"]:

        params["a"] = st.sidebar.number_input(
            "Left Endpoint",
            value=1.0
        )

        params["b"] = st.sidebar.number_input(
            "Right Endpoint",
            value=2.0
        )

    elif algorithm == "Secant":

        params["x0"] = st.sidebar.number_input(
            "First Guess",
            value=1.0
        )

        params["x1"] = st.sidebar.number_input(
            "Second Guess",
            value=2.0
        )

    elif algorithm == "Fixed Point":

        params["x0"] = st.sidebar.number_input(
            "Initial Guess",
            value=1.0
        )

        st.sidebar.info(
            "Enter g(x) instead of f(x)."
        )


    # -------------------------
    # Solve Button
    # -------------------------

    solve = st.sidebar.button(
        "Solve",
        use_container_width=True
    )

    compare = False


# ============================================================
# COMPARE ALGORITHMS MODE
# ============================================================

else:

    st.sidebar.subheader("Comparison")

    equation = st.sidebar.text_input(
        "Equation",
        "x**3 - x - 1"
    )

    tolerance = st.sidebar.number_input(
        "Tolerance",
        value=1e-6,
        format="%.8f"
    )

    max_iterations = st.sidebar.number_input(
        "Maximum Iterations",
        min_value=1,
        value=100
    )

    x0 = st.sidebar.number_input(
        "Initial Guess",
        value=1.5
    )

    a = st.sidebar.number_input(
        "Left Endpoint",
        value=1.0
    )

    b = st.sidebar.number_input(
        "Right Endpoint",
        value=2.0
    )

    st.sidebar.markdown("### Algorithms")

    compare_algorithms = []

    if st.sidebar.checkbox(
        "Newton-Raphson",
        value=True
    ):
        compare_algorithms.append("Newton-Raphson")

    if st.sidebar.checkbox(
        "Bisection",
        value=True
    ):
        compare_algorithms.append("Bisection")

    if st.sidebar.checkbox(
        "False Position",
        value=True
    ):
        compare_algorithms.append("False Position")

    if st.sidebar.checkbox(
        "Secant",
        value=True
    ):
        compare_algorithms.append("Secant")


    if len(compare_algorithms) == 0:

        st.sidebar.warning(
            "Select at least one algorithm."
        )


    compare = st.sidebar.button(
        "Compare Algorithms",
        use_container_width=True,
        disabled=len(compare_algorithms) == 0
    )

    solve = False


# ============================================================
# SOLVE SINGLE ALGORITHM
# ============================================================

if solve:

    try:

        method = ALGORITHMS[algorithm]

        result = method(params)

        # Save result so it survives Streamlit reruns
        st.session_state.result = result
        st.session_state.equation = equation

    except Exception as e:

        st.session_state.result = None

        st.error(str(e))


# ============================================================
# DISPLAY SINGLE ALGORITHM RESULT
# ============================================================

if (
    mode == "Single Algorithm"
    and st.session_state.result is not None
):

    result = st.session_state.result
    equation = st.session_state.equation

    st.success(
        "Computation completed successfully."
    )


    # -------------------------
    # Result Metrics
    # -------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Root",
            f"{result['root']:.10f}"
        )

    with col2:

        st.metric(
            "Iterations",
            result["iteration_count"]
        )

    with col3:

        st.metric(
            "Converged",
            "Yes" if result["converged"] else "No"
        )


    st.divider()


    # -------------------------
    # Tabs
    # -------------------------

    tab1, tab2, tab3 = st.tabs(
        [
            "📈 Visualization",
            "📋 Iteration Table",
            "🎬 Animation"
        ]
    )


    # ========================================================
    # VISUALIZATION TAB
    # ========================================================

    with tab1:

        fig = plot_iterations(
            equation,
            result["iterations"],
            result["root"]
        )

        st.pyplot(
            fig,
            use_container_width=True
        )


    # ========================================================
    # ITERATION TABLE TAB
    # ========================================================

    with tab2:

        st.dataframe(
            result["iterations"],
            use_container_width=True
        )


    # ========================================================
    # ANIMATION TAB
    # ========================================================

    with tab3:

        st.subheader(
            "Iteration Animation"
        )

        st.write(
            "Watch the numerical method approach the root "
            "iteration by iteration."
        )

        play_animation = st.button(
            "▶ Play Animation",
            key="play_animation"
        )

        if play_animation:

            placeholder = st.empty()

            frames = create_animation_frames(
                equation,
                result["iterations"]
            )

            for frame in frames:

                placeholder.pyplot(
                    frame,
                    clear_figure=True
                )

                time.sleep(0.4)

            st.success(
                "Animation completed!"
            )


# ============================================================
# COMPARE ALGORITHMS
# ============================================================

if compare:

    results = []


    for algo in compare_algorithms:


        # -------------------------
        # Newton-Raphson
        # -------------------------

        if algo == "Newton-Raphson":

            params = {

                "equation": equation,

                "x0": x0,

                "tolerance": tolerance,

                "max_iterations": max_iterations
            }


        # -------------------------
        # Bisection
        # -------------------------

        elif algo == "Bisection":

            params = {

                "equation": equation,

                "a": a,

                "b": b,

                "tolerance": tolerance,

                "max_iterations": max_iterations
            }


        # -------------------------
        # False Position
        # -------------------------

        elif algo == "False Position":

            params = {

                "equation": equation,

                "a": a,

                "b": b,

                "tolerance": tolerance,

                "max_iterations": max_iterations
            }


        # -------------------------
        # Secant
        # -------------------------

        elif algo == "Secant":

            params = {

                "equation": equation,

                "x0": a,

                "x1": b,

                "tolerance": tolerance,

                "max_iterations": max_iterations
            }


        # -------------------------
        # Execute Algorithm
        # -------------------------

        try:

            method = ALGORITHMS[algo]

            result = method(params)

            results.append(result)

        except Exception as e:

            st.warning(
                f"{algo}: {e}"
            )


    # ========================================================
    # DISPLAY COMPARISON
    # ========================================================

    if results:

        st.header(
            "Algorithm Comparison"
        )


        st.dataframe(
            comparison_table(results),
            use_container_width=True
        )


        st.pyplot(
            plot_convergence(results),
            use_container_width=True
        )