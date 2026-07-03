You are a machine learning engineer preparing training data for a Physics-Informed Neural Network (PINN). You have a pipeline that takes noisy observational data, extracts initial conditions, runs a forward numerical simulation, and evaluates statistical bounds on the generated data.

However, your C-based numerical integrator is producing garbage data because it diverges due to a faulty step-size adaptation scheme. 

Your task is to fix the pipeline.

**Files provided:**
1. `/home/user/observations.txt`: A flat file containing 500 space-separated floating-point numbers.
2. `/home/user/integrator.c`: A C program intended to process the observations and integrate the dynamical system $dy/dt = -y^2$.

**Requirements:**

1. **Observational Data Reshaping:** Modify `integrator.c` to read the 500 floats from `observations.txt` and reshape them logically into a 2D array of 100 rows and 5 columns. For each row, calculate the mean of its 5 values. These 100 mean values are your 100 initial conditions ($y_0$) at $t=0$.
2. **Fix the Numerical Integrator:** The current `integrator.c` has a buggy adaptive Euler method that diverges. Fix the integration loop to integrate each of the 100 initial conditions from $t=0.0$ to $t=1.0$ using a strictly fixed step size of `dt = 0.001` (exactly 1000 steps).
3. **Numerical Differentiation:** After integration, calculate the exact numerical derivative $dy/dt$ at $t=1.0$ for each trajectory (using the governing ODE). 
4. **C Output:** Make the C program output the 100 final derivatives (one per line) to `/home/user/derivatives.txt`. Compile and run your fixed C program.
5. **Bootstrap Confidence Interval:** Write a Python script at `/home/user/calc_ci.py` that reads `/home/user/derivatives.txt` and calculates the 95% bootstrap confidence interval of the mean of these derivatives. 
   - Use `scipy.stats.bootstrap` on the 1D data array.
   - Pass the arguments: `confidence_level=0.95`, `n_resamples=9999`, `method='percentile'`, and set the random state using `random_state=np.random.default_rng(42)`.
   - The script must write the result to `/home/user/ci.txt` in the exact format: `[lower_bound, upper_bound]` rounded to 4 decimal places (e.g., `[-0.1234, -0.1201]`). Run this Python script.