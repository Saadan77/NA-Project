import numpy as np

def trapezoidal_rule(x_values, y_values):
    """
    Calculate the integral using the Trapezoidal Rule for a series of points.
    :param x_values: List of x-values (e.g., time steps).
    :param y_values: List of y-values (e.g., positions at corresponding time steps).
    :return: Approximate integral (total distance covered).
    """
    if len(x_values) != len(y_values) or len(x_values) < 2:
        raise ValueError("x_values and y_values must have the same length and contain at least two values.")
    
    integral = 0
    for i in range(len(x_values) - 1):
        h = x_values[i + 1] - x_values[i]
        integral += h * (y_values[i] + y_values[i + 1]) / 2  # Trapezoidal calculation

    return integral

def linear_regression(x, slope, intercept):
    """
    Calculate the linear regression output.
    :param x: Input value (e.g., score).
    :param slope: Rate of change of difficulty with score.
    :param intercept: Starting difficulty at score 0.
    :return: Calculated difficulty factor.
    """
    return slope * x + intercept

def bisection_method(func, a, b, tol=1e-5, max_iter=100):
    """
    Implements the Bisection method to find the root of the function `func`.
    Args:
        func: The function for which we are finding the root.
        a, b: The interval [a, b] where the function changes sign.
        tol: The tolerance for convergence.
        max_iter: The maximum number of iterations before stopping.
    Returns:
        The estimated root of the function.
    """
    if func(a) * func(b) >= 0:
        raise ValueError("The function must change signs over the interval [a, b].")
    
    iter_count = 0
    while (b - a) / 2 > tol and iter_count < max_iter:
        c = (a + b) / 2
        if func(c) == 0:
            return c
        elif func(c) * func(a) < 0:
            b = c
        else:
            a = c
        iter_count += 1
        
    return (a + b) / 2
