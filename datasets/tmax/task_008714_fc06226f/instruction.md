I need you to help me set up a notebook-based workflow for a numerical simulation. I am a researcher studying thermal diffusion on a microchip using the 2D Heat Equation:

∂T/∂t = α(∂²T/∂x² + ∂²T/∂y²) + Q(x,y)

You need to create a Jupyter Notebook at `/home/user/heat_sim.ipynb` that performs a convergence and numerical stability test for this simulation, and then execute it. 

Here are the specific requirements for the simulation:
1. **Domain**: A 2D square domain from x=0 to x=1 and y=0 to y=1.
2. **Grid**: Use a uniform grid with N spatial steps in both x and y directions. The grid should have dimensions (N+1) × (N+1). So, dx = dy = 1.0 / N. Coordinates are x_i = i*dx, y_j = j*dy.
3. **Parameters**: Thermal diffusivity α = 0.05. 
4. **Source Term**: Q(x,y) = 50 if (0.4 <= x <= 0.6) and (0.4 <= y <= 0.6). Otherwise, Q(x,y) = 0.
5. **Initial & Boundary Conditions**: Initial temperature T = 0 everywhere. The boundaries (x=0, x=1, y=0, y=1) are kept perfectly cooled at T = 0 for all time.
6. **Time Integration**: Use the explicit forward Euler method. 
7. **Numerical Stability**: For a given N, the theoretical maximum stable time step is dt_max = (dx² * dy²) / (2*α*(dx² + dy²)) = dx² / (4*α). To ensure stability, use dt = 0.8 * dt_max.
8. **Duration**: Run the simulation for exactly M time steps, where M = ceil(0.1 / dt). (Use `math.ceil`).

Your notebook must do the following:
- Implement the simulation using `numpy` (multi-dimensional array manipulation).
- Run the simulation for two resolutions: N=20 and N=40 to test for convergence.
- Calculate the center point temperature for both resolutions at the final time step. The center point is at integer indices `(N/2, N/2)`.
- Export the results to a JSON file at `/home/user/sim_results.json`.

The JSON file must have exactly this structure:
```json
{
  "dt_max_N20": <float>,
  "dt_max_N40": <float>,
  "T_center_N20": <float>,
  "T_center_N40": <float>
}
```

Once you have written the notebook, install any necessary dependencies (e.g., `jupyter`, `nbconvert`, `numpy`) and execute the notebook headlessly from the command line using `jupyter nbconvert --to notebook --execute /home/user/heat_sim.ipynb`. Ensure the JSON file is successfully created.