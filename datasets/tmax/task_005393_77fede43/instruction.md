You are acting as a data scientist analyzing a high-resolution spectroscopy signal. You have been provided with a Python script `/home/user/analyze.py` that contains the mathematical model of a sharp absorption peak (`f_model(x)`) and its analytical derivative (`f_prime(x)`).

Currently, the script attempts to calculate the total area under the peak in the domain `x = 0.0` to `x = 10.0` using a custom adaptive Simpson's rule numerical integrator. However, because the peak is incredibly narrow and offset from the center of the domain, the initial coarse mesh evaluates to near-zero everywhere. The step-size adaptation falsely assumes the function is flat and never refines the mesh, resulting in an area calculation of approximately 0.

Your task:
1. **Nonlinear Equation Solving:** Edit `/home/user/analyze.py` to mathematically find the exact peak center. Do this by solving for the root of the derivative `f_prime(x) = 0` within the interval `[4.0, 5.0]` using an appropriate solver (e.g., `scipy.optimize.brentq` or `root_scalar`).
2. **Mesh Refinement / Domain Decomposition:** Fix the integration step. You can achieve this by explicitly decomposing the integration domain (e.g., integrating from `0` to `peak_center` and `peak_center` to `10`) so the integrator is forced to evaluate exactly at the peak, OR by modifying the `adaptive_simpson` function to enforce a minimum recursion depth before it is allowed to return.
3. Calculate the exact peak center and the total area.
4. **Automation:** Create a Bash script `/home/user/run_analysis.sh` that executes your Python code and writes the final results to `/home/user/results.txt`. The bash script should be executable.

The file `/home/user/results.txt` must contain exactly two lines in the following format (values rounded to 6 decimal places):
```
Peak Center: <value>
Total Area: <value>
```

Constraints:
- Do not use external integration libraries like `scipy.integrate.quad` for the final area calculation; you must fix or properly utilize the provided `adaptive_simpson` function.