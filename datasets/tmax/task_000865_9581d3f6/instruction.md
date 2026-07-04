You are a machine learning engineer preparing training data for a neural network surrogate model that predicts the steady-state of a diffusion process. Your goal is to build a reproducible data generation pipeline using Rust.

You are provided with a file `/home/user/initial_conditions.csv` containing 10 rows. Each row represents a 1D initial temperature profile $u(x, 0)$ discretized over 50 spatial points on the domain $x \in [0, 1]$. 

Your task is to write a Rust program that reads these initial conditions and simulates the 1D heat equation $u_t = \alpha u_{xx}$ for each profile using the explicit Forward-Time Central-Space (FTCS) finite difference method until it converges to a steady state. Finally, you must save the converged profiles into an HDF5 file.

Here are the exact physical and numerical parameters:
- Thermal diffusivity: $\alpha = 0.01$
- Spatial domain: $x \in [0, 1]$ with $N_x = 50$ points (index 0 to 49, so $\Delta x = 1.0 / 49.0$).
- Boundary conditions: Fixed at 0.0 at both ends ($u_0 = 0.0$ and $u_{49} = 0.0$ for all $t$).
- Time step: $\Delta t = 0.0001$.
- Convergence criterion: The simulation for a given profile is considered converged when the maximum absolute difference between consecutive time steps across all spatial points is strictly less than $10^{-6}$ (i.e., $\max_i |u_i^{n+1} - u_i^n| < 10^{-6}$).

Requirements:
1. Create a Cargo project named `diffusion_data` in `/home/user/diffusion_data`.
2. Write the simulation code in Rust. You may use external crates like `csv`, `ndarray`, and `hdf5` (assume `libhdf5-dev` is already installed on the system).
3. The program should output an HDF5 file at `/home/user/training_data.h5`.
4. The HDF5 file must contain a single dataset at the root level named `converged_states` of shape `(10, 50)` containing 64-bit floating-point numbers. Row $i$ in the dataset should correspond to the converged state of row $i$ from the CSV.
5. Create a shell script `/home/user/run_pipeline.sh` that, when executed, builds your Rust project in release mode and runs it to produce the final `training_data.h5` file.

Make sure your script is executable (`chmod +x /home/user/run_pipeline.sh`) and your pipeline runs without manual intervention.