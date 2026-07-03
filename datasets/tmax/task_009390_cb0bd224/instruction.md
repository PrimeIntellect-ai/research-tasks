You are a Machine Learning Engineer preparing a simulated physics dataset to train a Physics-Informed Neural Network (PINN). The data represents the temperature distribution in a 1D rod over time, modeled by the 1D Heat Equation.

Your task is to write and execute a Python script (`/home/user/generate_pinn_data.py`) that performs the following:

1. **Domain Decomposition Simulation:**
   - Solve $\frac{\partial u}{\partial t} = \alpha \frac{\partial^2 u}{\partial x^2}$ with $\alpha = 0.1$.
   - Spatial domain: $x \in [0, 1]$ divided into $Nx = 20$ intervals (i.e., 21 spatial points: index 0 to 20).
   - Time domain: $t \in [0, 0.2]$.
   - Initial condition: $u(x, 0) = \sin(\pi x)$.
   - Boundary conditions: $u(0, t) = u(1, t) = 0$.
   - Simulate using the Explicit Euler finite difference method. To apply domain decomposition, update the interior points of the "Left" domain (indices 1 to 9) and the "Right" domain (indices 11 to 19) independently at each time step. Then, update the interface point (index 10) using its neighbors (indices 9 and 11).

2. **Numerical Stability Testing & Temporal Mesh Refinement:**
   - Explicit Euler is conditionally stable. Start your simulation with $Nt = 2$ time intervals (i.e., 3 time points including $t=0$).
   - After running the simulation to $t=0.2$, check the maximum value of the temperature $u$ across the rod at the final time step. 
   - If the maximum value is $> 2.0$ (indicating numerical explosion/instability), double the number of time intervals ($Nt \leftarrow Nt \times 2$) and rerun the entire simulation.
   - Repeat this refinement until the maximum value of $u$ at the final time step is $\le 2.0$. Record this stable $Nt$.

3. **Bootstrap Confidence Intervals:**
   - Once you have the stable final temperature distribution array (21 points at $t=0.2$), simulate noisy sensor readings.
   - Set `numpy.random.seed(42)`.
   - Add Gaussian noise to the final state vector: `u_noisy = u_final + np.random.normal(0, 0.05, 21)`.
   - Now, calculate the 95% bootstrap confidence interval for the *mean* of `u_noisy`.
   - Reset `numpy.random.seed(42)` immediately before the bootstrap loop.
   - Perform exactly 10,000 bootstrap iterations (resample `u_noisy` with replacement 10,000 times, calculate the mean of each resample).
   - Compute the 2.5th and 97.5th percentiles of these 10,000 means using `numpy.percentile`.

4. **Output Verification:**
   - Save your final results to a JSON file at `/home/user/results.json`.
   - The JSON must have exactly the following keys:
     - `"stable_Nt"`: (integer) The number of time intervals where stability was first reached.
     - `"mean_noisy"`: (float) The mean of the `u_noisy` array.
     - `"ci_lower"`: (float) The 2.5th percentile of the bootstrap means.
     - `"ci_upper"`: (float) The 97.5th percentile of the bootstrap means.

Ensure all Python dependencies (like `numpy`) are installed in your environment before running your script.