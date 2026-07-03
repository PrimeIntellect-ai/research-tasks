You are a Machine Learning Engineer preparing training data for a Physics-Informed Neural Network (PINN). You have a Python script that generates 1D thermal diffusion data, but the script is currently failing to produce usable data because the numerical integrator diverges (producing `NaN`s) due to an incorrect step-size adaptation and a coarse spatial mesh.

Your task is to fix the simulation, generate the correct data, process raw observational data, and compare them.

**Step 1: Fix the Simulation**
There is a script located at `/home/user/generate_data.py`. It simulates the 1D Heat Equation $u_t = \alpha u_{xx}$ using the explicit Forward Euler method. 
- Currently, it uses a coarse mesh (`Nx = 10`) and a time step (`dt = 0.1`) that violates the CFL stability condition, causing divergence.
- Modify the script to use a refined spatial mesh of `Nx = 50` points (where $x \in [0, 1]$).
- Change the time step to `dt = 0.005` to ensure numerical stability.
- Run the script. It is programmed to save the final temperature profile at $t = 0.5$ as a NumPy array to `/home/user/simulated_profile.npy`.

**Step 2: Reshape Observational Data**
You have been provided with a reference observational dataset at `/home/user/obs_data.csv`. This file contains three columns: `id`, `raw_x`, and `raw_temp`. The rows are shuffled.
- Read this CSV file.
- Sort and extract the `raw_temp` values so they correspond exactly to the increasing spatial grid points $x$ of your refined `Nx = 50` simulation. (The `raw_x` values in the CSV exactly match the `Nx=50` `np.linspace(0, 1, 50)` grid, just out of order).

**Step 3: Curve Fitting and Comparison**
- Fit a 2nd-degree polynomial ($ax^2 + bx + c$) to your **simulated** temperature profile (Simulated $u$ vs. $x$).
- Calculate the Mean Squared Error (MSE) between the **simulated** temperature profile and the sorted **observational** temperature data.

**Step 4: Save Results**
Create a JSON file at `/home/user/results.json` containing the exact following keys:
- `"poly_coeffs"`: A list of the 3 polynomial coefficients from your fit in descending order of power (i.e., `[a, b, c]`).
- `"mse"`: The calculated MSE as a float.