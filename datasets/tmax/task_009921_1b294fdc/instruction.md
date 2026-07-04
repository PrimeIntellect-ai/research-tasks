You are acting as a performance engineer profiling a numerical application. 

You have been handed a 2D heat equation solver written in C++ (`/home/user/heat_sim.cpp`). The previous engineer recently refined the spatial mesh (increasing the grid resolution) to improve accuracy, but now the simulation diverges and produces `NaN` values. The issue is a classic step-size adaptation failure: the time step `dt` is hardcoded and violates the Courant-Friedrichs-Lewy (CFL) stability condition for the new spatial resolution.

Your task is to fix the simulation, run it, compare its output to a reference dataset, and perform a statistical analysis of the errors.

Perform the following steps:
1. **Fix the C++ Simulator**: Inspect `/home/user/heat_sim.cpp`. Look for the variable `dt`. Update the code so that `dt` is dynamically calculated based on the spatial steps `dx` and `dy`, and the thermal diffusivity `alpha`. Use the formula: `dt = 0.2 * std::min(dx * dx, dy * dy) / alpha;`.
2. **Compile and Run**: Compile the fixed C++ code (e.g., `g++ -O3 heat_sim.cpp -o heat_sim`) and run it. The simulation will output its final state to `/home/user/output.csv`. The CSV contains the temperature values on the 2D grid flattened into a single column (row-major order).
3. **Reference Dataset Comparison**: You are provided with `/home/user/reference.csv`, which contains the expected high-precision results (single column format, same size). Calculate the absolute difference (residual) between your `output.csv` and `reference.csv` at each grid point.
4. **Bootstrap Confidence Interval**: Write a Python script to compute the 95% bootstrap confidence interval of the **mean** of these absolute residuals. 
    - Use exactly `10000` bootstrap resamples.
    - Set the random seed to `42` (using `numpy.random.seed(42)`).
    - Use the percentile method (2.5th and 97.5th percentiles) to determine the lower and upper bounds of the confidence interval.
5. **Reporting**: Write the lower and upper bounds of the 95% confidence interval to a file named `/home/user/report.txt` in the exact format:
   `CI: [lower_bound, upper_bound]`
   (Round the bounds to 6 decimal places).

Note: Do not modify the grid size, domain boundaries, or initial conditions in the C++ file. Only fix the `dt` calculation.