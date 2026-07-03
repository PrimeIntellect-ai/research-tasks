You are a bioinformatics analyst studying the spatial spread of a novel genetic sequence variant across a 1D habitat. You hypothesize that the variant's spread over time and space follows the Fisher-KPP equation (a reaction-diffusion PDE):

∂u/∂t = D (∂²u/∂x²) + r u (1 - u)

Where:
- u(x,t) is the variant frequency at position x ∈ [0, 1] and time t.
- D = 0.01 is the diffusion coefficient.
- r = 0.5 is the growth rate.

Boundary and Initial Conditions:
- Initial condition: u(x, 0) = exp(-100 * (x - 0.5)²)
- Boundary conditions: Neumann (∂u/∂x = 0 at x=0 and x=1)
- The simulation runs from t = 0 to t = 2.0.

Your task is to write a script (in any language you choose, e.g., Python) to perform the following:

1. **PDE Numerical Solving & Matrix Decomposition:** Implement an implicit finite difference solver (e.g., Implicit Euler or Crank-Nicolson) to solve this PDE. Your solver must construct the sparse linear system and solve it at each time step using a matrix decomposition method (like LU or Cholesky). Use a time step of Δt = 0.002 (so 1000 steps).
2. **Convergence Testing:** Run your solver at two different spatial grid resolutions: 
   - Coarse: Nx = 51 (so Δx = 1/50)
   - Fine: Nx = 101 (so Δx = 1/100)
   Compute the maximum absolute error (L-infinity norm) between the coarse and fine solutions at t = 2.0. (Compare the points that exist in both grids).
3. **Probability Distribution Distance:** We have observed variant frequency data at t = 2.0. The file `/home/user/observed_variant.csv` contains two columns: `x` and `observed_u`.
   Normalize both the fine grid solution (Nx=101 at t=2.0) and the observed data so that they sum to 1.0 (treating them as discrete probability distributions over x). Compute the 1D Wasserstein distance (Earth Mover's Distance) between these two discrete distributions. Note: map the observed u points to the nearest x-coordinate in the fine grid if necessary, or compute the distance directly using a standard library function like `scipy.stats.wasserstein_distance`.

Write your results to a JSON file at `/home/user/results.json` with the following structure:
```json
{
  "convergence_error": <float>,
  "wasserstein_distance": <float>
}
```

You are responsible for installing any dependencies you need (e.g., `pip install numpy scipy`). Provide the code, run it, and generate the final JSON file.