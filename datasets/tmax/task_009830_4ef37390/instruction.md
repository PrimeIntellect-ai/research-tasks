You are a bioinformatics analyst working on modeling the population dynamics of genetic sequence variants over continuous time. 

You have been handed a workspace in `/home/user/analysis/` containing two files:
1. `input_profiles.npy`: A 100x500 NumPy array representing 100 different sequence profiles, each with 500 initial allele frequencies.
2. `sim_pop.py`: A script that simulates the continuous-time evolution of these frequencies.

Currently, the numerical integrator in `sim_pop.py` uses a naive Euler method with a fixed, excessively large step size. Because the underlying ordinary differential equation (ODE) is mathematically stiff, the current solver diverges, yielding infinities and NaNs.

Your task is to fix the numerical instability, parallelize the workload, and perform statistical density estimation on the converged results:

1. **Dependency Management**: Install any necessary Python packages (e.g., `scipy`, `numpy`) required for the tasks below.
2. **Fix the Numerical Integrator**: Modify `sim_pop.py` to replace the custom Euler loop with `scipy.integrate.solve_ivp`. You must use the `BDF` (Backward Differentiation Formula) method to handle the stiff dynamics properly. Integrate from `t=0` to `t=10`. Keep the exact mathematical definition of the derivative function (`gene_dynamics`) intact.
3. **Parallel Computing**: Processing 100 profiles sequentially is too slow. Modify the script to process the 100 profiles in parallel using Python's `multiprocessing.Pool` with exactly 4 worker processes.
4. **Density Estimation**: For each of the 100 profiles, extract the final state array (the 500 allele frequencies at `t=10`). Fit a Gaussian Kernel Density Estimator (`scipy.stats.gaussian_kde` using default bandwidth) to this 500-element array. Evaluate the estimated probability density function (PDF) precisely at the value `x = 0.5`.
5. **Output**: Create a JSON file at `/home/user/analysis/final_metrics.json` containing a single dictionary. This dictionary must have a key `"kde_at_05"` mapped to a list of the 100 evaluated density values (as floats). The list must maintain the exact order of the original 100 profiles from `input_profiles.npy`.

Ensure your final script runs successfully and produces the valid JSON file without manual intervention.