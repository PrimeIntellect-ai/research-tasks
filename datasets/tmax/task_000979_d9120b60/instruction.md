You are a machine learning engineer tasked with preparing an augmented training dataset for a neural network that predicts epidemic parameters from time-series data. You have been provided with a single noisy experimental dataset, and you need to generate multiple smoothed, realistic trajectories by sampling from the estimated parameter distribution.

The system follows the SIR model:
dS/dt = -beta * S * I / N
dI/dt = (beta * S * I / N) - gamma * I
dR/dt = gamma * I

Total population N = 1000. Initial conditions: S(0) = 990, I(0) = 10, R(0) = 0.

Your tasks:
1. Set up a Python virtual environment at `/home/user/env` and install `numpy`, `scipy`, `pandas`, and `matplotlib`.
2. Write a Python script `/home/user/augment.py` that reads the noisy experimental data from `/home/user/data/experimental.csv`.
3. Fit the SIR model to the infected compartment (`I` column) of the experimental data using `scipy.optimize.curve_fit` to estimate `beta` and `gamma` and their covariance matrix. Ensure your ODE solver uses the time points from the CSV. Bounds for both parameters should be [0.001, 1.0]. Initial guess: beta=0.5, gamma=0.2.
4. Using `numpy.random.seed(42)` and `numpy.random.multivariate_normal`, draw exactly 5 samples of the parameter pair (beta, gamma) from the estimated posterior (the fit parameters and covariance).
5. For each of the 5 sampled parameter pairs, solve the ODE for t in [0, 50] (51 evenly spaced points from 0 to 50 inclusive).
6. Save a CSV file to `/home/user/output/augmented_I.csv` containing the time points and the simulated `I` trajectories. The columns must be exactly: `t, I_0, I_1, I_2, I_3, I_4` (where `I_0` is the trajectory from the first sampled parameter pair, `I_1` from the second, etc.). Round the output values to 4 decimal places.
7. Generate a plot `/home/user/output/trajectories.png` showing the original noisy `I` data as scatter points and the 5 simulated `I` trajectories as lines.

Ensure the `output` directory is created before writing to it.