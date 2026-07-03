I am preparing a dataset to train a Physics-Informed Neural Network (PINN) on the dynamics of a damped harmonic oscillator. We collected a batch of raw sensor datasets, located in `/home/user/sensor_data/`. Unfortunately, some of the sensors were malfunctioning or miscalibrated, producing invalid data.

I need your help to filter out the bad runs by comparing them against the theoretical numerical solution.

Please perform the following steps:
1. Create a Python virtual environment at `/home/user/venv` and install the necessary scientific packages (`numpy`, `scipy`, `pandas`).
2. Write a Python script at `/home/user/filter_data.py` that solves the following second-order Ordinary Differential Equation (ODE) for the damped harmonic oscillator:
   `x''(t) + 0.2 x'(t) + 5.0 x(t) = 0`
   with initial conditions: `x(0) = 1.0` and `x'(0) = 0.0`.
3. Evaluate the ODE solution over the time interval `t = 0` to `t = 10`. The time steps in the sensor CSV files exactly match the time steps you should evaluate (there are exactly 101 evenly spaced points from 0 to 10 inclusive). Use `scipy.integrate.solve_ivp` with default tolerances.
4. For each CSV file in `/home/user/sensor_data/` (which contains `time` and `x_measured` columns), compute the Mean Squared Error (MSE) between the theoretical `x(t)` from your ODE solution and the `x_measured` data.
5. Identify the files where the MSE is strictly less than `0.05`.
6. Write the exact filenames (just the basenames, e.g., `run_0.csv`, not the full paths) of the valid runs to `/home/user/valid_runs.txt`. Sort the filenames alphabetically and print one filename per line.

Do not include any header or extra text in `/home/user/valid_runs.txt`.