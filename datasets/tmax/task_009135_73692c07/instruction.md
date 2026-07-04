You are an assistant helping a computational physics researcher investigate the numerical stability and convergence of a 1D heat equation solver. 

We are solving the 1D diffusion equation:
∂u/∂t = α (∂²u/∂x²)

On the domain x ∈ [0, 1] with boundary conditions u(0,t) = 0 and u(1,t) = 0, and initial condition u(x,0) = sin(πx).
The thermal diffusivity is α = 0.1.

The exact analytical solution is:
u_exact(x,t) = sin(πx) * exp(-π² * α * t)

We will use an explicit finite difference scheme:
u_i^{n+1} = u_i^n + (α * dt / dx²) * (u_{i+1}^n - 2u_i^n + u_{i-1}^n)

Your task is to write a Bash orchestration script at `/home/user/run_study.sh` that performs mesh refinement, numerical stability testing, and analytical validation. You may use standard Unix tools (like `awk`, `bc`, or inline `python3 -c` for floating-point math) inside your bash script.

The script `/home/user/run_study.sh` must do the following:
1. Loop over three mesh resolutions: N = 10, N = 20, and N = 40. Here, N is the number of spatial intervals, so there are N+1 grid points (i = 0, 1, ..., N) with dx = 1.0 / N.
2. For each N, calculate the theoretical maximum stable time step for this explicit scheme: dt_max = dx² / (2α).
3. Define a "stable" time step: dt_stable = 0.9 * dt_max.
4. Define an "unstable" time step: dt_unstable = 1.1 * dt_max.
5. For both time steps (stable and unstable), calculate the number of time steps required to reach *at least* t = 0.5. Specifically, M = ceiling(0.5 / dt). The actual end time will be t_end = M * dt.
6. Run the numerical simulation from step n=0 to n=M for both the stable and unstable configurations.
   - For the stable run, calculate the Mean Absolute Error (MAE) between the numerical solution and the analytical solution at t_end across all interior points (i=1 to N-1).
   - For the unstable run, find the maximum absolute value of u at t_end across all points. Due to numerical instability, this value should be large.
7. Append the results for each N to a log file at `/home/user/study_results.log` in the following comma-separated format (exactly one line per N, in increasing order of N):
   `N,dt_stable,MAE_stable,dt_unstable,max_abs_unstable`

Format the floating-point outputs to exactly 6 decimal places (e.g., using printf "%.6f").

Constraints:
- Do not use external libraries that require installation (e.g., no `pip install`). Use built-in Python 3 (`math` module) or `awk`/`bc`.
- Make sure `/home/user/run_study.sh` is executable and creates `/home/user/study_results.log` when run.