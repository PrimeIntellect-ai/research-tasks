You are an AI assistant helping a researcher optimize a numerical simulation. 

The researcher is studying the optimization of a 2D potential energy surface defined by the function:
`f(x, y) = x^2 + 50y^2`

They want to use standard gradient descent to find the minimum of this function, simulating the trajectories of 1000 independent particles. The initial coordinates of these 1000 particles are provided in `/home/user/init.txt` (each line contains `x0 y0` separated by a space).

However, they are struggling with numerical stability and performance. You need to write a C program that achieves the following:

1. **Analytical Stability Analysis**: Determine the theoretical maximum stable learning rate `alpha_max` for standard gradient descent on this exact function `f(x,y)`. (This is the threshold where the coordinate with the highest curvature begins to strictly diverge). Once you analytically find `alpha_max`, you must set your simulation's learning rate to exactly `alpha = alpha_max - 0.001`.
2. **Optimization**: Implement standard gradient descent: `pos_new = pos_old - alpha * gradient`.
3. **Parallelization**: Write the simulation in a C file located at `/home/user/sim.c`. Read the 1000 initial points from `/home/user/init.txt`. Use OpenMP (`#pragma omp parallel for`) to compute the gradient descent trajectories of all 1000 particles concurrently. 
4. **Simulation Details**: Run exactly `100` iterations of gradient descent for each particle. 
5. **Validation**: After the 100 iterations, calculate the final energy `E = x_100^2 + 50*y_100^2` for each particle. Calculate the arithmetic mean of this final energy across all 1000 particles. 

Output this final mean energy to a file named `/home/user/mean_energy.txt`. The file should contain *only* the mean energy formatted to exactly 6 decimal places (e.g., `0.012345`).

You may write, compile, and execute the C program to find the answer. The system has `gcc` and standard libraries installed.