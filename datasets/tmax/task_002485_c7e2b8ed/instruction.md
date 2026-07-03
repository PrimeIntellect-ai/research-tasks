You are a performance engineer optimizing a physics application. The application frequently solves a 1D boundary value problem (BVP) modeling a localized heat source, but the current numerical integrator often fails to resolve the peak or takes too long because it relies on the solver's default step-size adaptation (which is poorly suited for the localized sharp changes).

You need to write an improved solver and perform a statistical analysis on historical performance data.

**Phase 1: Statistical Analysis of Historical Data**
We have logged the number of iterations the old solver took before failing or converging in `/home/user/historical_runs.txt`. 
1. Write a Python script to compute the 95% bootstrap confidence interval for the **mean** number of iterations from this dataset.
2. Use exactly 10,000 resamples.
3. Use `numpy.random.seed(42)` immediately before the resampling loop or vectorized resampling. Randomly sample with replacement using standard numpy functions.
4. Calculate the 2.5th and 97.5th percentiles (using `numpy.percentile`) of the bootstrap means to form the lower and upper bounds.
5. Save the output to `/home/user/bootstrap_results.json` as a JSON object with keys `"lower_bound"` and `"upper_bound"`. Round the values to 2 decimal places.

**Phase 2: Improved BVP Solver with Domain Decomposition**
The BVP is defined on the domain $x \in [0, 1]$ as:
$u''(x) + f(x) = 0$
With boundary conditions:
$u(0) = 0, \quad u(1) = 0$
The heat source $f(x)$ is highly localized:
$f(x) = 100$ if $0.4 \le x \le 0.6$, and $0$ otherwise.

1. Write a Python script `/home/user/solve_bvp_pde.py` that solves this system using `scipy.integrate.solve_bvp`.
2. To overcome the step-size adaptation issue, you must manually implement a domain decomposition for the initial mesh. Provide an initial mesh `x` to `solve_bvp` that explicitly allocates more resolution to the active region. The mesh must consist of exactly:
   - 11 uniformly spaced points from 0.0 to 0.4
   - 51 uniformly spaced points from 0.4 to 0.6
   - 11 uniformly spaced points from 0.6 to 1.0
   *(Ensure there are no duplicate points where the regions overlap. The total number of unique points should be 71.)*
3. Use an initial guess of zeros for $u$ and $u'$.
4. Evaluate the computed solution object at $x = 0.5$. Save this single float value, rounded to 4 decimal places, to a file named `/home/user/bvp_result.txt`.

Ensure your scripts run cleanly in the terminal and produce exactly the required output files.