You are a data scientist working on fitting a dynamical model to observational data. 

You have been provided with a dataset of particle trajectories in `/home/user/data/observations.dat`. The file is a raw binary file containing double-precision floats. It represents the trajectories of 10 independent particles over 100 time steps. The data was written out from a C array flattened in row-major order with dimensions `[10 particles][100 time steps]`.

We are trying to fit a simplified physical model to this data. All particles follow the same underlying Ordinary Differential Equation (ODE):
dy/dt = -p_0 * y + p_1 * sin(y)

All particles start at y(0) = 5.0 at t=0. The time steps correspond to t = 0.0, 0.1, 0.2, ..., 9.9 (dt = 0.1).

We have an initial script at `/home/user/src/model_fit.c` that attempts to find the best parameters `p_0` and `p_1` using a grid search (searching p_0 in [0.0, 5.0] and p_1 in [0.0, 5.0] with 50 steps each). However, the script is flawed:
1. **Observational Data Reshaping:** The skeleton code incorrectly reads or indexes the multi-dimensional array, assuming it was `[100 time steps][10 particles]`. You need to fix the multi-dimensional array manipulation so the data is compared correctly against the simulated trajectories.
2. **Numerical Stability:** The script uses a basic Euler integrator with a step size equal to the observation interval (dt = 0.1). For certain parameters evaluated during the grid search, this step size is too large and the numerical integration diverges (producing NaNs or infinities), ruining the optimization. You must fix the integrator to ensure numerical stability (e.g., by implementing internal sub-stepping, dividing the dt=0.1 interval into 10 smaller integration steps of 0.01).
3. **Density Estimation / Distribution Fitting:** After finding the optimal `p_0` and `p_1` (the ones that minimize the Mean Squared Error across all particles and time steps), you need to estimate the noise distribution. Calculate the standard deviation of the residuals (observation - model_prediction) for the best-fit model.

Your task:
1. Modify `/home/user/src/model_fit.c` to fix the array indexing, fix the numerical integrator's stability, and compute the residual standard deviation.
2. Compile and run your fixed code.
3. Write the results to a file named `/home/user/solution.txt`. The file must contain exactly one line with three comma-separated values (formatted to 4 decimal places):
   `p_0, p_1, residual_stddev`

Constraints:
- Do not change the grid search boundaries or resolution (50 steps between 0.0 and 5.0 inclusive means step size of 0.10204...).
- Write your C code using standard libraries (`math.h`, `stdio.h`, `stdlib.h`).