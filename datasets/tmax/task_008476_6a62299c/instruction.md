You are a performance engineer profiling a numerical integrator that is exhibiting subtle divergence issues. You suspect that the adaptive step-size controller is misbehaving, causing the error to scale poorly with the step size.

An automated profiling run has generated an HDF5 file at `/home/user/simulation_data.h5` containing the execution trace. The integrator was solving the ordinary differential equation (ODE):
$dy/dt = -5y$
with the initial condition $y(0) = 1$.

The HDF5 file contains three datasets at the root level:
- `time`: The time steps $t$ at which the solution was evaluated.
- `step_size`: The step size $h$ used by the integrator to reach that time step.
- `y_numeric`: The computed numerical solution $y_{num}$ at each time step.

Your task is to write and execute a Python script to analyze this divergence:
1. Load the `time`, `step_size`, and `y_numeric` arrays from the HDF5 file.
2. Calculate the exact analytical solution $y_{analytical}$ for the given ODE at each time step.
3. Compute the absolute error between $y_{numeric}$ and $y_{analytical}$ at each time step.
4. Fit a 2nd-degree polynomial to model the absolute error as a function of the step size (i.e., $\text{error} = c_0 h^2 + c_1 h + c_2$). Use `numpy.polyfit` (which returns coefficients in decreasing order of power).
5. Calculate the Wasserstein distance between the distribution of $y_{numeric}$ values and the distribution of $y_{analytical}$ values to quantify the overall divergence. Use `scipy.stats.wasserstein_distance`.

Finally, output your results to a JSON file at `/home/user/profiling_report.json` with the exact following structure:
```json
{
  "polyfit_coefficients": [c_0, c_1, c_2],
  "wasserstein_distance": 0.000000
}
```
Replace the placeholders with your computed floats. Do not round the floats.

Ensure you install any necessary Python packages (like `h5py`, `numpy`, `scipy`) before running your script.