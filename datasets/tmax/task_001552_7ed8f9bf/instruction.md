You are a scientific computing assistant helping a researcher run parallel simulations of a 1D diffusion process to study the numerical stability and distributional spread of a pollutant.

Your goal is to write and execute an MPI-parallelized Python script that solves the 1D Diffusion equation using the Forward Time Centered Space (FTCS) finite difference scheme. You will sweep over a set of diffusion coefficients ($\alpha$) to test for numerical stability and, for the stable runs, measure how much the pollutant has spread using the Wasserstein distance.

**Physical and Numerical Setup:**
- Domain: $x \in [0, 1]$ discretized into exactly $N_x = 50$ points (including boundaries). So $\Delta x = 1/49$.
- Time: $t \in [0, T_{end}]$ where $T_{end} = 0.1$.
- Time step: $\Delta t = 0.001$ ($N_t = 100$ steps).
- PDE: $\frac{\partial u}{\partial t} = \alpha \frac{\partial^2 u}{\partial x^2}$
- Boundary Conditions: $u(0, t) = u(1, t) = 0$ (Dirichlet).
- Initial Condition: $u(x, 0) = 1.0$ for indices $20 \le i \le 29$ (0-indexed), and $0.0$ everywhere else.

**Experiment Requirements:**
1. Use `mpi4py` to parallelize the sweep over four diffusion coefficients: $\alpha \in \{0.1, 0.2, 0.25, 0.3\}$. The script must be designed to run with exactly 4 MPI processes, where each rank handles exactly one $\alpha$ (Rank 0 handles 0.1, Rank 1 handles 0.2, etc.).
2. For each $\alpha$, step the FTCS scheme forward in time.
3. **Numerical Stability Testing**: At each time step, check if the maximum absolute value of $u$ exceeds `100.0` or contains any `NaN` values. If it does, the simulation has become numerically unstable. Stop the time-stepping for this $\alpha$ immediately.
4. **Distance Metric**: If the simulation is stable at the end of $T_{end}$, normalize the final concentration profile $u(x, T_{end})$ so that it sums to 1. Also normalize the initial condition $u(x, 0)$ so that it sums to 1. Calculate the 1D Wasserstein distance between these two normalized discrete distributions over the spatial coordinates $x$. (Use `scipy.stats.wasserstein_distance` where the distributions are treated as weights at positions $x$).
5. If the simulation was unstable, assign a distance value of `-1.0`.
6. Rank 0 must gather the `(alpha, distance)` pairs from all ranks and save them to `/home/user/results.csv`. The CSV should have no header, and be formatted strictly as:
   ```
   0.1,0.0123456789
   0.2,0.0456789123
   ...
   ```
   (Sort the output ascending by $\alpha$).

**Actionable Steps:**
- Install necessary dependencies (`mpi4py`, `scipy`, `numpy`, and system OpenMPI libraries if needed).
- Write the MPI script at `/home/user/diffusion_mpi.py`.
- Run the script using `mpirun -np 4 python3 /home/user/diffusion_mpi.py`.
- Ensure `/home/user/results.csv` is generated perfectly.