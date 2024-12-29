import numpy as np

def linear_regression(x, slope, intercept):
    """
    Calculate the linear regression output.
    :param x: Input value (e.g., score).
    :param slope: Rate of change of difficulty with score.
    :param intercept: Starting difficulty at score 0.
    :return: Calculated difficulty factor.
    """
    return slope * x + intercept

# Simpson's 1/3 Rule for numerical integration
def simpsons_one_third_rule(x_values, y_values):
    if len(x_values) != len(y_values):
        raise ValueError("x_values and y_values must be of the same length")
    
    # Ensure the number of points is odd (required for Simpson's 1/3 Rule)
    if len(x_values) % 2 == 0:
        raise ValueError("The number of points (x_values) should be odd for Simpson's 1/3 Rule.")

    h = (x_values[-1] - x_values[0]) / (len(x_values) - 1)
    integral = y_values[0] + y_values[-1]

    for i in range(1, len(x_values) - 1, 2):
        integral += 4 * y_values[i]

    for i in range(2, len(x_values) - 1, 2):
        integral += 2 * y_values[i]

    integral *= h / 3
    return integral

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

def fourth_order_rk_method(func, y0, t0, h, steps):
    """
    Fourth-Order Runge-Kutta (R-K) Method to solve ODEs.
    Args:
        func: The derivative function f(t, y).
        y0: Initial condition for y (score or level).
        t0: Initial time or independent variable.
        h: Step size.
        steps: Number of steps to integrate.
    Returns:
        List of (t, y) values.
    """
    t_values = [t0]
    y_values = [y0]

    for _ in range(steps):
        k1 = h * func(t_values[-1], y_values[-1])
        k2 = h * func(t_values[-1] + h / 2, y_values[-1] + k1 / 2)
        k3 = h * func(t_values[-1] + h / 2, y_values[-1] + k2 / 2)
        k4 = h * func(t_values[-1] + h, y_values[-1] + k3)
        
        y_next = y_values[-1] + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        t_next = t_values[-1] + h

        t_values.append(t_next)
        y_values.append(y_next)

    return t_values, y_values

def score_function(t, y):
    """
    Derivative for score: Increases based on time and current score.
    """
    base_increment = 10.0  # Base score increment
    time_factor = 0.5 * t  # Additional score based on time
    return base_increment + time_factor

def level_function(t, y):
    """
    Derivative for level: Level increases faster as time progresses.
    """
    base_growth = 0.5  # Adjusted base growth for levels
    time_influence = 0.05 * t  # Slower time-based growth factor
    return base_growth + time_influence
