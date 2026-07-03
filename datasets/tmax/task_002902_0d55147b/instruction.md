You are a machine learning engineer preparing a training dataset for a surrogate model. Your goal is to map the stability boundaries of a numerical ODE integrator.

The integrator often diverges (returns infinity or NaN) if the step size `dt` is set too high for a given set of system parameters `a` and `b`. 

We have provided a black-box simulation script and a set of parameters:
- **Simulator:** `/home/user/sim/integrator.py` 
  This module contains a function `integrate(a, b, dt)`. It returns a float representing the final simulation state. If the integrator diverges, it returns `float('inf')`.
- **Parameters:** `/home/user/sim/params.json`
  A JSON list of dictionaries containing `id`, `a`, and `b` values.

**Your Task:**
Write a script (in any language you choose) that acts as an optimization/search routine to find the **maximum stable step size** (`max_dt`) for each parameter set in `params.json`.

Constraints and Requirements:
1. You must search for `dt` in the range `[0.001, 1.000]` (inclusive).
2. The search precision must be exactly `0.001` (i.e., test 0.001, 0.002, ..., 1.000).
3. A step size is considered "stable" if `integrate(a, b, dt)` returns a finite value strictly less than `1000`.
4. Assume stability is monotonic: if a specific `dt` diverges, all larger `dt` values for those parameters will also diverge.
5. Save your results to a CSV file at `/home/user/optimal_dt.csv`.
6. The CSV must have exactly two columns: `id` and `max_dt` (with a header row). Format `max_dt` to exactly three decimal places (e.g., `0.550`).

Ensure your final output file `/home/user/optimal_dt.csv` is correctly formatted and contains the optimal step size for every parameter ID.