You are an AI assistant helping a computational physics researcher. The researcher needs you to build a complete pipeline that optimizes the "drift vector" for a group of particles navigating a 2D space with a trap and a target. You will use Monte Carlo simulation and an optimization algorithm.

Your task is to write and execute a Python script (`/home/user/optimize_drift.py`) that performs the following steps:

1. **Setup**: The script must use `numpy`, `scipy`, and `h5py`. You should install these dependencies in the system or a virtual environment as necessary.
2. **Monte Carlo Simulation**: Create a function that simulates the trajectories of $N=10,000$ particles for $T=20$ discrete time steps.
   - All particles start at the origin: $(0.0, 0.0)$.
   - At each time step, every *active* particle updates its position: $P_{t+1} = P_t + \Delta + V$.
   - $\Delta$ is a random 2D step where both x and y components are drawn independently from a standard normal distribution ($\mu=0, \sigma=1$).
   - $V = (v_x, v_y)$ is a constant 2D drift vector applied to all particles at all steps.
   - **The Trap**: There is a circular trap centered at $(4.0, 4.0)$ with a radius of $3.0$. If a particle ends a step at a distance $\le 3.0$ from $(4.0, 4.0)$, it becomes "trapped". A trapped particle stops moving entirely and its coordinates should be permanently set to `NaN` (i.e., `np.nan` for both x and y) for the remainder of the simulation and in the final output.
   - **The Target**: There is a circular target centered at $(10.0, 10.0)$ with a radius of $2.0$.
   - **Crucial Reproducibility Rule**: At the very beginning of *every* simulation run (i.e., inside the function that runs the simulation for a given $V$), you MUST reset the random seed using `np.random.seed(42)`. This ensures the optimizer explores the parameter space deterministically.
3. **Optimization**:
   - Use `scipy.optimize.minimize` with the `Nelder-Mead` method to find the optimal drift vector $V = (v_x, v_y)$ that maximizes the number of active particles located *inside* the target (distance $\le 2.0$ from $(10.0, 10.0)$) exactly at the end of step 20.
   - The objective function should return the negative of the number of particles in the target.
   - Use an initial guess of $v_x = 0.0, v_y = 0.0$.
4. **Data Output**:
   - Once the optimizer finishes, run the simulation one last time using the optimal drift vector (and `np.random.seed(42)`).
   - Save the results into an HDF5 file located at `/home/user/results.h5`.
   - The HDF5 file must contain the following datasets at the root level:
     - `optimized_v`: A 1D float64 array of length 2 containing the optimal $(v_x, v_y)$.
     - `final_positions`: A 2D float64 array of shape `(10000, 2)` containing the positions of the particles after the 20th step. (Trapped particles must have `NaN` values).
     - `target_count`: A single scalar integer dataset containing the number of particles that successfully reached the target at step 20 using the optimal drift.

Write the code, execute it to generate the `/home/user/results.h5` file, and ensure it is correct.