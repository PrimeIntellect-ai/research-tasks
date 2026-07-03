You are acting as a computational data scientist. We need to fit a 1D spatial diffusion-reaction model (Fisher's equation) to some observational data, simulating the spread of a biological population.

The governing PDE is:
∂u/∂t = D * (∂²u/∂x²) + r * u * (1 - u)
Where:
- D = 0.1 (diffusion coefficient)
- r = 1.0 (growth rate)
- Domain: x ∈ [0, 10]
- Boundary conditions: Zero-flux (Neumann) at x = 0 and x = 10.
- Initial condition at t = 0: u(x, 0) = exp(-x²)

We have a local, proprietary Rust ODE solver package located at `/app/rk4-solver`. It uses the Runge-Kutta 4th order method. However, a junior developer recently touched the code and reported that the solver's output is "slightly off." You must inspect `/app/rk4-solver/src/lib.rs`, find the mathematical error in the RK4 implementation, and fix it.

Once the solver is fixed, create a new Rust project at `/home/user/fisher_sim` that uses `/app/rk4-solver` as a local dependency. 
Your Rust program should:
1. Implement the spatial domain as a 1D graph/mesh.
2. Use the method of lines (finite difference for the spatial Laplacian) to convert the PDE into a system of ODEs.
3. Solve the system from t = 0 to t = 5.0 using the fixed RK4 solver.

We have observational data of the population at t = 5.0, provided in `/home/user/observations.jsonl` (each line is a JSON object with weirdly shaped keys, e.g., `{"coord_x": 1.2, "measured_pop_level": 0.45}`).
You need to:
1. Reshape and parse this observational data.
2. Refine your spatial mesh resolution (Δx) and time step (Δt) in your simulation until the Mean Squared Error (MSE) between your simulated `u(x, 5.0)` and the observational data at the exact same `x` coordinates is minimized.

When you are done, run your simulation and save the final computed state at t = 5.0 to `/home/user/final_state.csv` with exactly two columns: `x` and `u`. (Output `x` values should at least include the coordinates from the observational data so we can verify the fit).

We will automatically evaluate your result by computing the Mean Squared Error against a high-resolution reference solution. Your simulation must achieve an MSE of less than 0.001.