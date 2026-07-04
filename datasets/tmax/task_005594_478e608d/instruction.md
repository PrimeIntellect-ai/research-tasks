You are a performance engineer working on a particle physics simulation. A previous team member wrote a Monte Carlo simulation script that integrated particle trajectories, but it was notoriously slow and eventually diverged (returned NaNs) because they used a handwritten, fixed-step Euler integrator that failed on steep potential gradients.

Your task is to write a robust, performant replacement using Python, incorporating proper adaptive numerical integration and scientific data I/O. 

Specifically, you need to create a Python script at `/home/user/mc_integrator.py` that does the following:
1. Opens the HDF5 file `/home/user/input_states.h5` (which already exists) and reads the dataset `/states`. This dataset contains 1000 initial conditions for particles. Each row is `(x0, v0)`.
2. For each particle, integrates the equations of motion for a non-linear oscillator:
   dx/dt = v
   dv/dt = -x^3
   Integrate from t = 0 to t = 5.0.
3. You MUST use an adaptive step-size ODE solver (like `scipy.integrate.solve_ivp` with the 'RK45' method) to prevent the divergence issues that plagued the previous implementation.
4. Collect the final states (x, v) at t = 5.0 for all 1000 particles.
5. Save the final states to a new HDF5 file at `/home/user/output_states.h5` under the dataset name `/final_states` (shape should be 1000x2, stored as float64).
6. Calculate the Monte Carlo average of the final position (the 'x' coordinate) across all 1000 particles.
7. Write this average to `/home/user/avg_x.txt`, rounded to exactly 4 decimal places (e.g., `0.1234`).

You may need to install standard scientific Python libraries (like `numpy`, `scipy`, `h5py`) before running your script. Ensure your script executes successfully and generates the required files.