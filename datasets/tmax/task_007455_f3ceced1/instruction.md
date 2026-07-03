You are acting as a data scientist working on modeling a chemical reaction network: A -> B -> C.

You have been given a partially complete Python script located at `/home/user/kinetics/fit_kinetics.py`. This script attempts to model the kinetics of the reaction and fit the rate constants ($k_1$ for A->B, and $k_2$ for B->C) to a reference dataset located at `/home/user/kinetics/reference.csv`.

Currently, there are two major problems:
1. The custom numerical integrator (`euler_integrate`) in the script uses a fixed step size that is too large, causing numerical instability (divergence or unphysical oscillations) when the optimization algorithm explores certain regions of the parameter space.
2. The optimization loop using `scipy.optimize.minimize` is incomplete. 

Your task:
1. Fix the numerical integration step so that it is stable. You can modify the step size to be sufficiently small (e.g., `dt = 0.01`) or replace it entirely with a robust solver like `scipy.integrate.solve_ivp`.
2. Complete the objective function and optimization call to fit $k_1$ and $k_2$ by minimizing the Sum of Squared Errors (SSE) between the simulated concentration of B and the reference concentration of B at the corresponding time points. Use the Nelder-Mead method with an initial guess of `[1.0, 1.0]`.
3. Save the optimally fitted parameters into a new file `/home/user/kinetics/optimal_params.txt`. The file should contain a single line with the two values separated by a comma, rounded to exactly two decimal places (e.g., `1.23,4.56`).

The initial concentrations are A=1.0, B=0.0, C=0.0.
The reference data is sampled at t = 0.0, 0.5, 1.0, 1.5, 2.0.