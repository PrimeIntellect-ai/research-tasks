You are assisting a computational physics researcher in validating a new 1D nonlinear finite difference solver. Before applying the solver to unknown problems, we need to validate it against a problem with a known analytical solution and verify its mesh convergence properties.

The nonlinear ordinary differential equation (ODE) we are solving is:
d²u/dx² - u(x)² = f(x)    for x in [0, 1]

With Dirichlet boundary conditions:
u(0) = 1
u(1) = e (Euler's number)

To make the analytical solution exactly u(x) = e^x, the source term f(x) is analytically derived as:
f(x) = e^x - e^(2x)

Your task is to:
1. Write a Python script at `/home/user/solve_ode.py` that solves this nonlinear ODE using a standard second-order central finite difference scheme. 
2. The domain x ∈ [0, 1] should be discretized into N equal intervals (i.e., N+1 grid points including boundaries: x_0, x_1, ..., x_N), so the step size is h = 1/N.
3. The discretization of the second derivative at interior points should be (u_{i-1} - 2u_i + u_{i+1}) / h². This will result in a system of nonlinear algebraic equations for the interior points.
4. Solve this nonlinear system using `scipy.optimize.fsolve` or `scipy.optimize.root` (using an initial guess of u_i = 1.0 for all interior points).
5. Perform a mesh refinement study by solving the system for N = 10, N = 20, N = 40, and N = 80.
6. For each N, calculate the Maximum Absolute Error (L_infinity norm) between your numerical solution and the exact analytical solution u(x) = e^x at the grid points.
7. Output the results to a CSV log file located at `/home/user/convergence.log`. 

The log file `/home/user/convergence.log` must have exactly the following format (including the header):
```csv
N,MaxError
10,<error_for_10>
20,<error_for_20>
40,<error_for_40>
80,<error_for_80>
```
Represent the error in scientific notation (e.g., 1.234567e-04). 

Execute your Python script to generate the log file.