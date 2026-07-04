You are a Machine Learning Engineer preparing synthetic training data for a Physics-Informed Neural Network (PINN). The PINN is being designed to learn the solution to a 1D nonlinear boundary value problem representing steady-state heat conduction with a nonlinear sink term.

Your task is to create a reproducible C++ pipeline that numerically solves the following nonlinear ODE using finite differences and Newton's method, and outputs the result as a dataset.

**Equation:**
$$- \frac{d^2u}{dx^2} + \exp(u) = 10$$
Domain: $x \in [0, 1]$
Boundary conditions: $u(0) = 0, \quad u(1) = 0$

**Instructions:**
1. Write a C++ program at `/home/user/generate_data.cpp` that:
   - Discretizes the domain $x \in [0, 1]$ into a uniform mesh of 101 points ($N=101$), so the step size $h = 0.01$.
   - Uses the standard second-order central finite difference scheme for the second derivative.
   - Solves the resulting system of nonlinear algebraic equations using the multidimensional Newton-Raphson method.
   - You must implement a simple tridiagonal linear solver (e.g., Thomas algorithm) to solve the Jacobian system at each Newton step. Do not use external linear algebra libraries (like Eigen) to ensure the code is self-contained.
   - Uses an initial guess of $u_i = 0$ for all $x_i$.
   - Iterates until the maximum absolute update (L-infinity norm of $\Delta u$) is less than $10^{-7}$.
2. The program must output the final solution to a CSV file at `/home/user/training_data.csv`.
   - The CSV must have a header: `x,u`
   - It should contain exactly 101 rows of data (plus the header), corresponding to $x_0 = 0.0$ to $x_{100} = 1.0$.
   - Output the floating-point numbers formatted to 6 decimal places.
3. Write a bash script `/home/user/run_pipeline.sh` that compiles the C++ program (using `g++ -O3`) and runs it to generate the CSV file.
4. Execute your pipeline so that `/home/user/training_data.csv` is produced.

Your final deliverables will be the `generate_data.cpp` file, the `run_pipeline.sh` script, and the resulting `training_data.csv` file.