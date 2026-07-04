You are assisting a data scientist in finding the steady-state of a nonlinear model used in a recent experiment. The steady-state is defined by the roots of the following system of nonlinear equations:

Equation 1: 2x - y + exp(-x) - 1 = 0
Equation 2: -x + 2y + sin(y) - 2 = 0

Your task is to write and execute a Python script to perform the following:
1. **Nonlinear Equation Solving:** Find the root (x, y) of the system using an initial guess of (x=0, y=0).
2. **Analytical Jacobian:** Derive the analytical Jacobian matrix of the system.
3. **Numerical Stability Testing:** Evaluate the analytical Jacobian matrix at the found root (x, y) and calculate its condition number (using the 2-norm, typically the default in `numpy.linalg.cond`).

Write your results to a JSON file located precisely at `/home/user/model_fit_results.json`. 
The JSON file must contain exactly the following keys with their corresponding floating-point values:
- `"x"`: The x-coordinate of the root.
- `"y"`: The y-coordinate of the root.
- `"condition_number"`: The condition number of the Jacobian evaluated at the root.

Ensure your Python script runs successfully and generates the requested JSON file. You may use standard scientific libraries like `numpy` and `scipy`.