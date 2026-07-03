You are a machine learning engineer preparing a training dataset for a Neural PDE solver. The data generation pipeline requires a robust numerical solver that generates solutions to the 1D Heat Equation under varying physical parameters and pushes the results to a caching layer. 

In your workspace at `/app/`, you have a multi-service setup. Currently, a Redis instance is running on port 6379. 

Your task is to write a Go web service in `/app/generator/` that acts as the PDE solver and data orchestrator.

Here are the requirements for the Go service:
1. It must listen for HTTP POST requests on `0.0.0.0:8080` at the `/solve` endpoint.
2. The endpoint will receive a JSON payload like this:
   `{"id": "sim_123", "alpha": 0.05, "t_end": 0.2}`
   where `alpha` is the thermal diffusivity and `t_end` is the final simulation time.
3. Upon receiving a request, the service must solve the 1D Heat Equation: 
   $\frac{\partial u}{\partial t} = \alpha \frac{\partial^2 u}{\partial x^2}$
   Domain: $x \in [0, 1]$
   Spatial grid: $N = 11$ evenly spaced points (i.e., $x_0 = 0, x_{10} = 1$, so $\Delta x = 0.1$).
   Initial condition: $u(x, 0) = 4x(1 - x)$
   Boundary conditions: $u(0, t) = 0$ and $u(1, t) = 0$ for all $t$.
4. **Numerical Method & Convergence Testing**:
   Use the explicit finite difference method (Forward Euler).
   Since Forward Euler has stability and accuracy constraints, you must implement a convergence loop:
   - Start with an initial time step $\Delta t = 0.05$.
   - Compute the solution at $t = t\_end$.
   - Re-compute the solution using a halved time step ($\Delta t / 2$).
   - Find the maximum absolute difference between the two solutions at $t = t\_end$ across all 11 spatial points.
   - If the maximum difference is greater than $10^{-4}$, halve the time step again and repeat the comparison (comparing $\Delta t / 4$ against $\Delta t / 2$, etc.) until the difference is $\le 10^{-4}$.
5. Once converged, the service must push the final computed solution (the array of 11 values at $t\_end$ from the finest time step) to the running Redis instance at `127.0.0.1:6379`. 
   - Use a Redis `RPUSH` operation to append the 11 float values (as strings) to a list key named `solution:<id>` (e.g., `solution:sim_123`).
6. The HTTP endpoint should then return a `200 OK` response.

Ensure your Go service is running in the background and listening on port 8080.