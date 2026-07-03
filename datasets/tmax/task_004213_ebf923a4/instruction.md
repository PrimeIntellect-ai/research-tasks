As a machine learning engineer, you are preparing a synthetic dataset of a nonlinear dynamical system to train a Physics-Informed Neural Network (PINN). 

Please write a C program at `/home/user/simulate.c` that performs the following:

1. **Numerical Integration**: Numerically integrates the nonlinear Ordinary Differential Equation (ODE):
   `dx/dt = -x^3 + cos(t)`
   from `t = 0` to `t = 5` with the initial condition `x(0) = 0.5`. Use the standard 4th-order Runge-Kutta (RK4) method with a fixed time step of `dt = 0.01`.

2. **Dataset Generation**: Save the resulting trajectory to `/home/user/trajectory.csv`. The file should have a header `t,x` and contain the values at each step from `t=0` to `t=5` (inclusive), printed to 4 decimal places (e.g., `0.0100,0.5098`).

3. **Nonlinear Equation Solving**: Find the first time `t > 0` where the trajectory crosses zero (i.e., `x(t) = 0`). Use linear interpolation between the two consecutive integration steps where `x` changes sign to estimate the exact crossing time.

4. **Output**: Write this estimated crossing time `t` to a file at `/home/user/root.txt`, formatted to 4 decimal places (e.g., `1.2345`).

Compile and run your C program to produce the required output files (`/home/user/trajectory.csv` and `/home/user/root.txt`). You can use `gcc` and link the math library if necessary.