from algorithms.newton import newton_method
from algorithms.bisection import bisection_method
from algorithms.false_position import false_position_method
from algorithms.secant import secant_method
from algorithms.fixed_point import fixed_point_method


ALGORITHMS = {

    "Newton-Raphson": newton_method,

    "Bisection": bisection_method,

    "False Position": false_position_method,

    "Secant": secant_method,

    "Fixed Point": fixed_point_method

}